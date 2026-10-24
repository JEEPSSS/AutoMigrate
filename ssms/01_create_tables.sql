/* =====================================================================
   SC2207 Lab 5 - TEL3 Team 3 - TechPulse
   01_create_tables.sql : DDL (run on database tel3g3)
   Changes vs Lab 3 (per TA feedback / Lab 5 needs):
     - SERVICE_TICKET no longer stores Client_ID (derivable via DEVICE)
     - BILLING_STATEMENT stores Service_Ticket_ID directly (UNIQUE);
       redundant GENERATES relation removed
     - WARRANTY_CLAIM no longer stores Client_ID (derivable via BILL)
     - DEVICE gets IMEI_Serial_No (real-world unique id, candidate key)
     - TECHNICIAN gets Name
     - SERVICE_TICKET gets nullable Warranty_Claim_ID (rework jobs, Q5)
     - PROCEDURE renamed REPAIR_PROCEDURE (PROCEDURE is a T-SQL keyword)
   ===================================================================== */

-- Drop in child-to-parent order so the script can be re-run
IF OBJECT_ID('trg_PartAllocation_Guard','TR') IS NOT NULL DROP TRIGGER trg_PartAllocation_Guard;
IF OBJECT_ID('SERVICE_TICKET','U') IS NOT NULL AND OBJECT_ID('FK_Ticket_Claim','F') IS NOT NULL
    ALTER TABLE SERVICE_TICKET DROP CONSTRAINT FK_Ticket_Claim;
DROP TABLE IF EXISTS WARRANTY_CLAIM;
DROP TABLE IF EXISTS BILLING_STATEMENT;
DROP TABLE IF EXISTS CREATES;
DROP TABLE IF EXISTS RESTOCK_REQUEST;
DROP TABLE IF EXISTS PURCHASE_ORDER;
DROP TABLE IF EXISTS VENDOR;
DROP TABLE IF EXISTS PART_ALLOCATION;
DROP TABLE IF EXISTS PART;
DROP TABLE IF EXISTS WORK_SESSION;
DROP TABLE IF EXISTS DIAGNOSTIC_ASSESSMENT;
DROP TABLE IF EXISTS REPAIR_PROCEDURE;
DROP TABLE IF EXISTS SERVICE_TICKET;
DROP TABLE IF EXISTS TECHNICIAN;
DROP TABLE IF EXISTS WORKSTATION;
DROP TABLE IF EXISTS DEVICE;
DROP TABLE IF EXISTS DEVICE_TYPE;
DROP TABLE IF EXISTS CLIENT;
GO

/* ---------- Requirement 1: Device intake & front desk ---------- */
CREATE TABLE CLIENT (
    Client_ID               INT           NOT NULL,
    Name                    VARCHAR(100)  NOT NULL,
    Address                 VARCHAR(200)  NOT NULL,
    Type                    VARCHAR(10)   NOT NULL,
    Contact_Details         VARCHAR(20)   NOT NULL,
    Email                   VARCHAR(100)  NOT NULL,
    Account_Creation_Date   DATE          NOT NULL,
    PRIMARY KEY (Client_ID),
    CONSTRAINT UQ_Client_Email UNIQUE (Email),
    CONSTRAINT CK_Client_Type CHECK (Type IN ('Retail','Corporate'))
);

CREATE TABLE DEVICE_TYPE (
    Model_ID                        INT           NOT NULL,
    Model_Name                      VARCHAR(60)   NOT NULL,
    Device_Category                 VARCHAR(20)   NOT NULL,
    Manufacturer_Name               VARCHAR(40)   NOT NULL,
    Manufacturer_Warranty_Duration  INT           NOT NULL,   -- months
    PRIMARY KEY (Model_ID),
    CONSTRAINT CK_DeviceType_Category CHECK (Device_Category IN
        ('Smartphone','Tablet','Smartwatch','Earbuds','Headphones')),
    CONSTRAINT CK_DeviceType_Warranty CHECK (Manufacturer_Warranty_Duration >= 0)
);

CREATE TABLE DEVICE (
    Device_ID         INT           NOT NULL,
    IMEI_Serial_No    VARCHAR(20)   NOT NULL,
    Description       VARCHAR(200)  NOT NULL,
    Colour            VARCHAR(30)   NOT NULL,
    Storage_Capacity  INT           NULL,          -- GB; NULL for audio wearables
    Model_ID          INT           NOT NULL,
    Client_ID         INT           NOT NULL,
    PRIMARY KEY (Device_ID),
    CONSTRAINT UQ_Device_IMEI UNIQUE (IMEI_Serial_No),
    CONSTRAINT CK_Device_Storage CHECK (Storage_Capacity IS NULL OR Storage_Capacity > 0),
    FOREIGN KEY (Model_ID)  REFERENCES DEVICE_TYPE(Model_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (Client_ID) REFERENCES CLIENT(Client_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

/* ---------- Requirement 2: Workshop allocation & assessment ---------- */
CREATE TABLE WORKSTATION (
    Workstation_ID    INT          NOT NULL,
    Workstation_Type  VARCHAR(40)  NOT NULL,
    Status            VARCHAR(12)  NOT NULL,
    PRIMARY KEY (Workstation_ID),
    CONSTRAINT CK_Workstation_Status CHECK (Status IN ('Occupied','Free','Maintenance'))
);

CREATE TABLE TECHNICIAN (
    Technician_ID                 INT           NOT NULL,
    Name                          VARCHAR(100)  NOT NULL,
    Primary_Specialisation        VARCHAR(20)   NOT NULL,
    Certification_Level           VARCHAR(10)   NOT NULL,
    Standard_Hourly_Billing_Rate  DECIMAL(6,2)  NOT NULL,
    PRIMARY KEY (Technician_ID),
    CONSTRAINT CK_Tech_Spec CHECK (Primary_Specialisation IN
        ('Display','Battery','Audio','Logic Board','Enclosure')),
    CONSTRAINT CK_Tech_Cert CHECK (Certification_Level IN ('Junior','Senior','Expert')),
    CONSTRAINT CK_Tech_Rate CHECK (Standard_Hourly_Billing_Rate > 0)
);

CREATE TABLE SERVICE_TICKET (
    Service_Ticket_ID       INT            NOT NULL,
    Problem_Desc            VARCHAR(200)   NOT NULL,
    Status                  VARCHAR(20)    NOT NULL,
    Date_Received           DATETIME       NOT NULL,
    Estimated_Repair_Cost   DECIMAL(10,2)  NOT NULL,
    Device_ID               INT            NOT NULL,
    Workstation_ID          INT            NOT NULL,
    Warranty_Claim_ID       INT            NULL,      -- set only for warranty rework jobs
    PRIMARY KEY (Service_Ticket_ID),
    CONSTRAINT CK_Ticket_Status CHECK (Status IN
        ('Received','Diagnosing','In Progress','Ready for Pickup','Completed')),
    CONSTRAINT CK_Ticket_Est CHECK (Estimated_Repair_Cost >= 0),
    FOREIGN KEY (Device_ID)      REFERENCES DEVICE(Device_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (Workstation_ID) REFERENCES WORKSTATION(Workstation_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE DIAGNOSTIC_ASSESSMENT (
    Assessment_ID          INT           NOT NULL,
    Health_Results         VARCHAR(30)   NOT NULL,
    Diagnostic_Error_Code  VARCHAR(20)   NULL,
    Action                 VARCHAR(200)  NOT NULL,
    Service_Ticket_ID      INT           NOT NULL,
    Technician_ID          INT           NOT NULL,
    PRIMARY KEY (Assessment_ID),
    CONSTRAINT UQ_Assess_Ticket UNIQUE (Service_Ticket_ID),   -- one assessment per ticket
    CONSTRAINT CK_Assess_Health CHECK (Health_Results IN
        ('Normal','Liquid Damage','Tripped','Battery Degraded','Physical Damage')),
    FOREIGN KEY (Service_Ticket_ID) REFERENCES SERVICE_TICKET(Service_Ticket_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Technician_ID) REFERENCES TECHNICIAN(Technician_ID)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

/* ---------- Requirement 3: Repair execution & labour ---------- */
CREATE TABLE REPAIR_PROCEDURE (
    Procedure_ID        INT           NOT NULL,
    Procedure_Type      VARCHAR(20)   NOT NULL,
    Procedure_Details   VARCHAR(200)  NOT NULL,
    Total_Time_Spent    INT           NOT NULL DEFAULT 0,   -- minutes, = SUM(WORK_SESSION.Billable_Time)
    Service_Ticket_ID   INT           NOT NULL,
    PRIMARY KEY (Procedure_ID),
    CONSTRAINT CK_Proc_Type CHECK (Procedure_Type IN
        ('Display','Battery','Audio','Logic Board','Enclosure')),
    CONSTRAINT CK_Proc_Time CHECK (Total_Time_Spent >= 0),
    FOREIGN KEY (Service_Ticket_ID) REFERENCES SERVICE_TICKET(Service_Ticket_ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE WORK_SESSION (
    Session_ID      INT       NOT NULL,
    Start_Time      DATETIME  NOT NULL,
    End_Time        DATETIME  NOT NULL,
    Billable_Time   INT       NOT NULL,     -- minutes
    Procedure_ID    INT       NOT NULL,
    Technician_ID   INT       NOT NULL,
    PRIMARY KEY (Session_ID),
    CONSTRAINT CK_Session_Times CHECK (End_Time > Start_Time),
    CONSTRAINT CK_Session_Billable CHECK (Billable_Time > 0),
    FOREIGN KEY (Procedure_ID)  REFERENCES REPAIR_PROCEDURE(Procedure_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Technician_ID) REFERENCES TECHNICIAN(Technician_ID)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

/* ---------- Requirement 4: Parts inventory & restocking ---------- */
CREATE TABLE PART (
    Part_Code                  VARCHAR(12)    NOT NULL,
    Item_Description           VARCHAR(100)   NOT NULL,
    Selling_Price              DECIMAL(10,2)  NOT NULL,
    Minimum_Reorder_Quantity   INT            NOT NULL,
    Part_Category              VARCHAR(20)    NOT NULL,
    Current_Quantity           INT            NOT NULL,
    PRIMARY KEY (Part_Code),
    CONSTRAINT CK_Part_Category CHECK (Part_Category IN
        ('Displays','Batteries','Audio Drivers','Enclosures','Flex Cables')),
    CONSTRAINT CK_Part_Price CHECK (Selling_Price > 0),
    CONSTRAINT CK_Part_Qty CHECK (Current_Quantity >= 0 AND Minimum_Reorder_Quantity >= 0)
);

CREATE TABLE PART_ALLOCATION (
    Allocated_ID         INT            NOT NULL,
    Procedure_ID         INT            NOT NULL,
    Quantity_Allocated   INT            NOT NULL,
    Locked_Unit_Price    DECIMAL(10,2)  NOT NULL,   -- price frozen at time of allocation
    Allocated_Time       DATETIME       NOT NULL,
    Part_Code            VARCHAR(12)    NOT NULL,
    PRIMARY KEY (Allocated_ID, Procedure_ID),
    CONSTRAINT CK_Alloc_Qty CHECK (Quantity_Allocated > 0),
    CONSTRAINT CK_Alloc_Price CHECK (Locked_Unit_Price >= 0),
    FOREIGN KEY (Procedure_ID) REFERENCES REPAIR_PROCEDURE(Procedure_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Part_Code) REFERENCES PART(Part_Code)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE VENDOR (
    Vendor_ID              INT           NOT NULL,
    Name                   VARCHAR(100)  NOT NULL,
    Phone_Number           VARCHAR(20)   NOT NULL,
    Email                  VARCHAR(100)  NOT NULL,
    Agreed_Payment_Terms   VARCHAR(10)   NOT NULL,
    PRIMARY KEY (Vendor_ID),
    CONSTRAINT CK_Vendor_Terms CHECK (Agreed_Payment_Terms IN ('Cash','Credit'))
);

CREATE TABLE PURCHASE_ORDER (
    Order_ID                INT            NOT NULL,
    Order_Date              DATE           NOT NULL,
    Order_Status            VARCHAR(10)    NOT NULL,
    Expected_Delivery_Date  DATE           NOT NULL,
    Total_Order_Cost        DECIMAL(12,2)  NOT NULL,
    Vendor_ID               INT            NOT NULL,
    PRIMARY KEY (Order_ID),
    CONSTRAINT CK_PO_Status CHECK (Order_Status IN ('Pending','Shipped','Received')),
    CONSTRAINT CK_PO_Dates CHECK (Expected_Delivery_Date >= Order_Date),
    CONSTRAINT CK_PO_Cost CHECK (Total_Order_Cost >= 0),
    FOREIGN KEY (Vendor_ID) REFERENCES VENDOR(Vendor_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE RESTOCK_REQUEST (
    Req_ID        INT          NOT NULL,
    Req_Date      DATE         NOT NULL,
    Quantity_Req  INT          NOT NULL,
    Part_Code     VARCHAR(12)  NOT NULL,
    PRIMARY KEY (Req_ID),
    CONSTRAINT CK_Req_Qty CHECK (Quantity_Req > 0),
    FOREIGN KEY (Part_Code) REFERENCES PART(Part_Code)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE CREATES (            -- restock requests combined into purchase orders
    Req_ID    INT  NOT NULL,
    Order_ID  INT  NOT NULL,
    PRIMARY KEY (Req_ID, Order_ID),
    FOREIGN KEY (Req_ID)   REFERENCES RESTOCK_REQUEST(Req_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Order_ID) REFERENCES PURCHASE_ORDER(Order_ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

/* ---------- Requirement 5: Billing & after-sales ---------- */
CREATE TABLE BILLING_STATEMENT (
    Bill_ID                 INT            NOT NULL,
    Billing_Date            DATE           NOT NULL,
    Total_Component_Costs   DECIMAL(10,2)  NOT NULL,
    Total_Labour_Charges    DECIMAL(10,2)  NOT NULL,
    Tax_Rates               DECIMAL(5,2)   NOT NULL,    -- percent, e.g. 9.00
    Discount                DECIMAL(10,2)  NOT NULL DEFAULT 0,
    Balance_Due             DECIMAL(10,2)  NOT NULL,
    Payment_Status          VARCHAR(10)    NOT NULL,
    Service_Ticket_ID       INT            NOT NULL,
    PRIMARY KEY (Bill_ID),
    CONSTRAINT UQ_Bill_Ticket UNIQUE (Service_Ticket_ID),
    CONSTRAINT CK_Bill_Status CHECK (Payment_Status IN ('Unpaid','Paid','Partial')),
    CONSTRAINT CK_Bill_Amounts CHECK (Total_Component_Costs >= 0 AND Total_Labour_Charges >= 0
                                      AND Discount >= 0 AND Balance_Due >= 0
                                      AND Tax_Rates BETWEEN 0 AND 100),
    FOREIGN KEY (Service_Ticket_ID) REFERENCES SERVICE_TICKET(Service_Ticket_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE WARRANTY_CLAIM (
    Claim_ID                 INT            NOT NULL,
    Fault_Description        VARCHAR(200)   NOT NULL,
    Review_Status            VARCHAR(15)    NOT NULL,
    Approved_Refund_Value    DECIMAL(10,2)  NULL,
    Requested_Refund_Value   DECIMAL(10,2)  NOT NULL,
    Approved_Remedy          VARCHAR(100)   NULL,
    Submission_Date          DATE           NOT NULL,
    Bill_ID                  INT            NOT NULL,
    PRIMARY KEY (Claim_ID),
    CONSTRAINT CK_Claim_Status CHECK (Review_Status IN ('Under Review','Approved','Rejected')),
    CONSTRAINT CK_Claim_Values CHECK (Requested_Refund_Value >= 0
        AND (Approved_Refund_Value IS NULL OR Approved_Refund_Value <= Requested_Refund_Value)),
    FOREIGN KEY (Bill_ID) REFERENCES BILLING_STATEMENT(Bill_ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

-- Rework tickets point back to the warranty claim that triggered them
ALTER TABLE SERVICE_TICKET ADD CONSTRAINT FK_Ticket_Claim
    FOREIGN KEY (Warranty_Claim_ID) REFERENCES WARRANTY_CLAIM(Claim_ID)
    ON DELETE NO ACTION ON UPDATE NO ACTION;
GO
