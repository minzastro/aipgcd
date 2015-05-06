
-- Table: keys
CREATE TABLE keys ( 
    [key]       CHAR( 25 )      NOT NULL,
    key_class   CHAR( 25 ),
    description VARCHAR( 400 ),
    data_format VARCHAR( 10 ) 
);


-- Table: source_types
CREATE TABLE source_types ( 
    type_id     INTEGER         PRIMARY KEY
                                NOT NULL,
    description VARCHAR( 200 ) 
);


-- Table: data_sources
CREATE TABLE data_sources ( 
    source      CHAR( 25 )      PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    description VARCHAR( 200 ),
    reference   VARCHAR( 100 ),
    type_id     INTEGER         REFERENCES source_types ( type_id ) 
);


-- Table: clusters
CREATE TABLE clusters ( 
    uid       INTEGER     PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE,
    ra        REAL        NOT NULL,
    dec       REAL        NOT NULL,
    source    CHAR( 25 )  NOT NULL
                          REFERENCES data_sources ( source ),
    source_id INT 
);


-- Table: threexmm_detections
CREATE TABLE threexmm_detections ( 
    DETID            INTEGER,
    SRCID            INTEGER,
    DR3SRCID         INTEGER,
    DR3DETID         INTEGER,
    DR3DETDIST       FLOAT,
    DR3SRCDIST       FLOAT,
    DR3MULT          INTEGER,
    IAUNAME          TEXT,
    SRC_NUM          INTEGER,
    OBS_ID           TEXT,
    REVOLUT          TEXT,
    MJD_START        DOUBLE PRECISION,
    MJD_STOP         DOUBLE PRECISION,
    OBS_CLASS        INTEGER,
    PN_FILTER        TEXT,
    M1_FILTER        TEXT,
    M2_FILTER        TEXT,
    PN_SUBMODE       TEXT,
    M1_SUBMODE       TEXT,
    M2_SUBMODE       TEXT,
    RA               DOUBLE PRECISION,
    DEC              DOUBLE PRECISION,
    POSERR           FLOAT,
    LII              DOUBLE PRECISION,
    BII              DOUBLE PRECISION,
    RADEC_ERR        FLOAT,
    SYSERRCC         FLOAT,
    REFCAT           INTEGER,
    POSCOROK         BOOL,
    RA_UNC           DOUBLE PRECISION,
    DEC_UNC          DOUBLE PRECISION,
    EP_1_FLUX        FLOAT,
    EP_1_FLUX_ERR    FLOAT,
    EP_2_FLUX        FLOAT,
    EP_2_FLUX_ERR    FLOAT,
    EP_3_FLUX        FLOAT,
    EP_3_FLUX_ERR    FLOAT,
    EP_4_FLUX        FLOAT,
    EP_4_FLUX_ERR    FLOAT,
    EP_5_FLUX        FLOAT,
    EP_5_FLUX_ERR    FLOAT,
    EP_8_FLUX        FLOAT,
    EP_8_FLUX_ERR    FLOAT,
    EP_9_FLUX        FLOAT,
    EP_9_FLUX_ERR    FLOAT,
    PN_1_FLUX        FLOAT,
    PN_1_FLUX_ERR    FLOAT,
    PN_2_FLUX        FLOAT,
    PN_2_FLUX_ERR    FLOAT,
    PN_3_FLUX        FLOAT,
    PN_3_FLUX_ERR    FLOAT,
    PN_4_FLUX        FLOAT,
    PN_4_FLUX_ERR    FLOAT,
    PN_5_FLUX        FLOAT,
    PN_5_FLUX_ERR    FLOAT,
    PN_8_FLUX        FLOAT,
    PN_8_FLUX_ERR    FLOAT,
    PN_9_FLUX        FLOAT,
    PN_9_FLUX_ERR    FLOAT,
    M1_1_FLUX        FLOAT,
    M1_1_FLUX_ERR    FLOAT,
    M1_2_FLUX        FLOAT,
    M1_2_FLUX_ERR    FLOAT,
    M1_3_FLUX        FLOAT,
    M1_3_FLUX_ERR    FLOAT,
    M1_4_FLUX        FLOAT,
    M1_4_FLUX_ERR    FLOAT,
    M1_5_FLUX        FLOAT,
    M1_5_FLUX_ERR    FLOAT,
    M1_8_FLUX        FLOAT,
    M1_8_FLUX_ERR    FLOAT,
    M1_9_FLUX        FLOAT,
    M1_9_FLUX_ERR    FLOAT,
    M2_1_FLUX        FLOAT,
    M2_1_FLUX_ERR    FLOAT,
    M2_2_FLUX        FLOAT,
    M2_2_FLUX_ERR    FLOAT,
    M2_3_FLUX        FLOAT,
    M2_3_FLUX_ERR    FLOAT,
    M2_4_FLUX        FLOAT,
    M2_4_FLUX_ERR    FLOAT,
    M2_5_FLUX        FLOAT,
    M2_5_FLUX_ERR    FLOAT,
    M2_8_FLUX        FLOAT,
    M2_8_FLUX_ERR    FLOAT,
    M2_9_FLUX        FLOAT,
    M2_9_FLUX_ERR    FLOAT,
    EP_8_RATE        FLOAT,
    EP_8_RATE_ERR    FLOAT,
    EP_9_RATE        FLOAT,
    EP_9_RATE_ERR    FLOAT,
    PN_1_RATE        FLOAT,
    PN_1_RATE_ERR    FLOAT,
    PN_2_RATE        FLOAT,
    PN_2_RATE_ERR    FLOAT,
    PN_3_RATE        FLOAT,
    PN_3_RATE_ERR    FLOAT,
    PN_4_RATE        FLOAT,
    PN_4_RATE_ERR    FLOAT,
    PN_5_RATE        FLOAT,
    PN_5_RATE_ERR    FLOAT,
    PN_8_RATE        FLOAT,
    PN_8_RATE_ERR    FLOAT,
    PN_9_RATE        FLOAT,
    PN_9_RATE_ERR    FLOAT,
    M1_1_RATE        FLOAT,
    M1_1_RATE_ERR    FLOAT,
    M1_2_RATE        FLOAT,
    M1_2_RATE_ERR    FLOAT,
    M1_3_RATE        FLOAT,
    M1_3_RATE_ERR    FLOAT,
    M1_4_RATE        FLOAT,
    M1_4_RATE_ERR    FLOAT,
    M1_5_RATE        FLOAT,
    M1_5_RATE_ERR    FLOAT,
    M1_8_RATE        FLOAT,
    M1_8_RATE_ERR    FLOAT,
    M1_9_RATE        FLOAT,
    M1_9_RATE_ERR    FLOAT,
    M2_1_RATE        FLOAT,
    M2_1_RATE_ERR    FLOAT,
    M2_2_RATE        FLOAT,
    M2_2_RATE_ERR    FLOAT,
    M2_3_RATE        FLOAT,
    M2_3_RATE_ERR    FLOAT,
    M2_4_RATE        FLOAT,
    M2_4_RATE_ERR    FLOAT,
    M2_5_RATE        FLOAT,
    M2_5_RATE_ERR    FLOAT,
    M2_8_RATE        FLOAT,
    M2_8_RATE_ERR    FLOAT,
    M2_9_RATE        FLOAT,
    M2_9_RATE_ERR    FLOAT,
    EP_8_CTS         FLOAT,
    EP_8_CTS_ERR     FLOAT,
    PN_8_CTS         FLOAT,
    PN_8_CTS_ERR     FLOAT,
    M1_8_CTS         FLOAT,
    M1_8_CTS_ERR     FLOAT,
    M2_8_CTS         FLOAT,
    M2_8_CTS_ERR     FLOAT,
    EP_8_DET_ML      FLOAT,
    EP_9_DET_ML      FLOAT,
    PN_1_DET_ML      FLOAT,
    PN_2_DET_ML      FLOAT,
    PN_3_DET_ML      FLOAT,
    PN_4_DET_ML      FLOAT,
    PN_5_DET_ML      FLOAT,
    PN_8_DET_ML      FLOAT,
    PN_9_DET_ML      FLOAT,
    M1_1_DET_ML      FLOAT,
    M1_2_DET_ML      FLOAT,
    M1_3_DET_ML      FLOAT,
    M1_4_DET_ML      FLOAT,
    M1_5_DET_ML      FLOAT,
    M1_8_DET_ML      FLOAT,
    M1_9_DET_ML      FLOAT,
    M2_1_DET_ML      FLOAT,
    M2_2_DET_ML      FLOAT,
    M2_3_DET_ML      FLOAT,
    M2_4_DET_ML      FLOAT,
    M2_5_DET_ML      FLOAT,
    M2_8_DET_ML      FLOAT,
    M2_9_DET_ML      FLOAT,
    EP_EXTENT        FLOAT,
    EP_EXTENT_ERR    FLOAT,
    EP_EXTENT_ML     FLOAT,
    EP_HR1           FLOAT,
    EP_HR1_ERR       FLOAT,
    EP_HR2           FLOAT,
    EP_HR2_ERR       FLOAT,
    EP_HR3           FLOAT,
    EP_HR3_ERR       FLOAT,
    EP_HR4           FLOAT,
    EP_HR4_ERR       FLOAT,
    PN_HR1           FLOAT,
    PN_HR1_ERR       FLOAT,
    PN_HR2           FLOAT,
    PN_HR2_ERR       FLOAT,
    PN_HR3           FLOAT,
    PN_HR3_ERR       FLOAT,
    PN_HR4           FLOAT,
    PN_HR4_ERR       FLOAT,
    M1_HR1           FLOAT,
    M1_HR1_ERR       FLOAT,
    M1_HR2           FLOAT,
    M1_HR2_ERR       FLOAT,
    M1_HR3           FLOAT,
    M1_HR3_ERR       FLOAT,
    M1_HR4           FLOAT,
    M1_HR4_ERR       FLOAT,
    M2_HR1           FLOAT,
    M2_HR1_ERR       FLOAT,
    M2_HR2           FLOAT,
    M2_HR2_ERR       FLOAT,
    M2_HR3           FLOAT,
    M2_HR3_ERR       FLOAT,
    M2_HR4           FLOAT,
    M2_HR4_ERR       FLOAT,
    PN_1_EXP         FLOAT,
    PN_2_EXP         FLOAT,
    PN_3_EXP         FLOAT,
    PN_4_EXP         FLOAT,
    PN_5_EXP         FLOAT,
    M1_1_EXP         FLOAT,
    M1_2_EXP         FLOAT,
    M1_3_EXP         FLOAT,
    M1_4_EXP         FLOAT,
    M1_5_EXP         FLOAT,
    M2_1_EXP         FLOAT,
    M2_2_EXP         FLOAT,
    M2_3_EXP         FLOAT,
    M2_4_EXP         FLOAT,
    M2_5_EXP         FLOAT,
    PN_1_BG          FLOAT,
    PN_2_BG          FLOAT,
    PN_3_BG          FLOAT,
    PN_4_BG          FLOAT,
    PN_5_BG          FLOAT,
    M1_1_BG          FLOAT,
    M1_2_BG          FLOAT,
    M1_3_BG          FLOAT,
    M1_4_BG          FLOAT,
    M1_5_BG          FLOAT,
    M2_1_BG          FLOAT,
    M2_2_BG          FLOAT,
    M2_3_BG          FLOAT,
    M2_4_BG          FLOAT,
    M2_5_BG          FLOAT,
    PN_1_VIG         FLOAT,
    PN_2_VIG         FLOAT,
    PN_3_VIG         FLOAT,
    PN_4_VIG         FLOAT,
    PN_5_VIG         FLOAT,
    M1_1_VIG         FLOAT,
    M1_2_VIG         FLOAT,
    M1_3_VIG         FLOAT,
    M1_4_VIG         FLOAT,
    M1_5_VIG         FLOAT,
    M2_1_VIG         FLOAT,
    M2_2_VIG         FLOAT,
    M2_3_VIG         FLOAT,
    M2_4_VIG         FLOAT,
    M2_5_VIG         FLOAT,
    PN_ONTIME        FLOAT,
    M1_ONTIME        FLOAT,
    M2_ONTIME        FLOAT,
    EP_ONTIME        FLOAT,
    PN_OFFAX         FLOAT,
    M1_OFFAX         FLOAT,
    M2_OFFAX         FLOAT,
    EP_OFFAX         FLOAT,
    PN_MASKFRAC      FLOAT,
    M1_MASKFRAC      FLOAT,
    M2_MASKFRAC      FLOAT,
    DIST_NN          FLOAT,
    SUM_FLAG         INTEGER,
    EP_FLAG          TEXT,
    PN_FLAG          TEXT,
    M1_FLAG          TEXT,
    M2_FLAG          TEXT,
    TSERIES          BOOL,
    SPECTRA          BOOL,
    EP_CHI2PROB      DOUBLE PRECISION,
    PN_CHI2PROB      DOUBLE PRECISION,
    M1_CHI2PROB      DOUBLE PRECISION,
    M2_CHI2PROB      DOUBLE PRECISION,
    PN_FVAR          DOUBLE PRECISION,
    PN_FVARERR       DOUBLE PRECISION,
    M1_FVAR          DOUBLE PRECISION,
    M1_FVARERR       DOUBLE PRECISION,
    M2_FVAR          DOUBLE PRECISION,
    M2_FVARERR       DOUBLE PRECISION,
    VAR_FLAG         BOOL,
    VAR_EXP_ID       TEXT,
    VAR_INST_ID      TEXT,
    SC_RA            DOUBLE PRECISION,
    SC_DEC           DOUBLE PRECISION,
    SC_POSERR        FLOAT,
    SC_DET_ML        FLOAT,
    SC_EP_1_FLUX     FLOAT,
    SC_EP_1_FLUX_ERR FLOAT,
    SC_EP_2_FLUX     FLOAT,
    SC_EP_2_FLUX_ERR FLOAT,
    SC_EP_3_FLUX     FLOAT,
    SC_EP_3_FLUX_ERR FLOAT,
    SC_EP_4_FLUX     FLOAT,
    SC_EP_4_FLUX_ERR FLOAT,
    SC_EP_5_FLUX     FLOAT,
    SC_EP_5_FLUX_ERR FLOAT,
    SC_EP_8_FLUX     FLOAT,
    SC_EP_8_FLUX_ERR FLOAT,
    SC_EP_9_FLUX     FLOAT,
    SC_EP_9_FLUX_ERR FLOAT,
    SC_HR1           FLOAT,
    SC_HR1_ERR       FLOAT,
    SC_HR2           FLOAT,
    SC_HR2_ERR       FLOAT,
    SC_HR3           FLOAT,
    SC_HR3_ERR       FLOAT,
    SC_HR4           FLOAT,
    SC_HR4_ERR       FLOAT,
    SC_EXTENT        FLOAT,
    SC_EXT_ML        FLOAT,
    SC_CHI2PROB      DOUBLE PRECISION,
    SC_FVAR          DOUBLE PRECISION,
    SC_FVARERR       DOUBLE PRECISION,
    SC_VAR_FLAG      BOOL,
    SC_SUM_FLAG      INTEGER,
    SC_EP_8_FMIN     FLOAT,
    SC_EP_8_FMIN_ERR FLOAT,
    SC_EP_8_FMAX     FLOAT,
    SC_EP_8_FMAX_ERR FLOAT,
    MJD_FIRST        DOUBLE PRECISION,
    MJD_LAST         DOUBLE PRECISION,
    N_DETECTIONS     INTEGER,
    CONFUSED         BOOL,
    HIGH_BACKGROUND  BOOL 
);


-- Table: threexmm_sources
CREATE TABLE threexmm_sources ( 
    SRCID            INTEGER,
    IAUNAME          TEXT,
    SC_RA            DOUBLE PRECISION,
    SC_DEC           DOUBLE PRECISION,
    SC_POSERR        FLOAT,
    SC_DET_ML        FLOAT,
    SC_EP_1_FLUX     FLOAT,
    SC_EP_1_FLUX_ERR FLOAT,
    SC_EP_2_FLUX     FLOAT,
    SC_EP_2_FLUX_ERR FLOAT,
    SC_EP_3_FLUX     FLOAT,
    SC_EP_3_FLUX_ERR FLOAT,
    SC_EP_4_FLUX     FLOAT,
    SC_EP_4_FLUX_ERR FLOAT,
    SC_EP_5_FLUX     FLOAT,
    SC_EP_5_FLUX_ERR FLOAT,
    SC_EP_8_FLUX     FLOAT,
    SC_EP_8_FLUX_ERR FLOAT,
    SC_EP_9_FLUX     FLOAT,
    SC_EP_9_FLUX_ERR FLOAT,
    SC_EP_8_FMIN     FLOAT,
    SC_EP_8_FMIN_ERR FLOAT,
    SC_EP_8_FMAX     FLOAT,
    SC_EP_8_FMAX_ERR FLOAT,
    SC_HR1           FLOAT,
    SC_HR1_ERR       FLOAT,
    SC_HR2           FLOAT,
    SC_HR2_ERR       FLOAT,
    SC_HR3           FLOAT,
    SC_HR3_ERR       FLOAT,
    SC_HR4           FLOAT,
    SC_HR4_ERR       FLOAT,
    SC_EXTENT        FLOAT,
    SC_EXT_ML        FLOAT,
    SC_CHI2PROB      DOUBLE PRECISION,
    SC_VAR_FLAG      BOOL,
    SC_SUM_FLAG      INTEGER,
    MJD_FIRST        DOUBLE PRECISION,
    MJD_LAST         DOUBLE PRECISION,
    SC_FVAR          DOUBLE PRECISION,
    SC_FVARERR       DOUBLE PRECISION,
    N_DETECTIONS     INTEGER,
    CONFUSED         BOOL,
    LEDAS_URL        TEXT 
);


-- Table: takey_table2
CREATE TABLE takey_table2 ( 
    recno    INTEGER,
    Seq      INTEGER,
    n_2XMM   TEXT,
    _2XMM    TEXT,
    ObsID    TEXT,
    z        FLOAT,
    q_z      TEXT,
    Scale    FLOAT,
    R500     FLOAT,
    Fcat     FLOAT,
    e_Fcat   FLOAT,
    Lcat     FLOAT,
    e_Lcat   FLOAT,
    L500     FLOAT,
    e_L500   FLOAT,
    M500     FLOAT,
    e_M500   FLOAT,
    T500     FLOAT,
    e_T500   FLOAT,
    objid    INTEGER,
    zp       FLOAT,
    zs       TEXT,
    Nzs      INTEGER,
    [offset] FLOAT,
    NED      TEXT,
    Refs     TEXT,
    Sloan    TEXT,
    DR8      TEXT,
    RAJ2000  DOUBLE PRECISION,
    DEJ2000  DOUBLE PRECISION,
    RABdeg   DOUBLE PRECISION,
    DEBdeg   DOUBLE PRECISION 
);


-- Table: takey_table1
CREATE TABLE takey_table1 ( 
    recno    INTEGER,
    Seq      INTEGER,
    n_2XMM   TEXT,
    _2XMM    TEXT,
    ObsID    TEXT,
    z        FLOAT,
    q_z      TEXT,
    Scale    FLOAT,
    Rap      FLOAT,
    R500     FLOAT,
    Tap      FLOAT,
    E_Tap    FLOAT,
    e_Tap_   FLOAT,
    Fap      FLOAT,
    E_Fap    FLOAT,
    e_Fap_   FLOAT,
    Lap      FLOAT,
    E_Lap    FLOAT,
    e_Lap_   FLOAT,
    L500     FLOAT,
    e_L500   FLOAT,
    M500     FLOAT,
    e_M500   FLOAT,
    nH       FLOAT,
    objid    INTEGER,
    zp       FLOAT,
    zs       TEXT,
    Nzs      INTEGER,
    [offset] FLOAT,
    NED      TEXT,
    Refs     TEXT,
    Sloan    TEXT,
    DR8      TEXT,
    RAJ2000  DOUBLE PRECISION,
    DEJ2000  DOUBLE PRECISION,
    RABdeg   DOUBLE PRECISION,
    DEBdeg   DOUBLE PRECISION 
);


-- Table: Rabitz_candidates
CREATE TABLE Rabitz_candidates ( 
    [Field-name]   TEXT,
    redshift       TEXT,
    ra             DOUBLE PRECISION,
    dec            DOUBLE PRECISION,
    [r-z (ISO)]    FLOAT,
    [r-z (APER)]   FLOAT,
    [r (ISO)]      FLOAT,
    [r_err (ISO)]  FLOAT,
    [r (APER)]     FLOAT,
    [r_err (APER)] FLOAT,
    [z (ISO)]      FLOAT,
    [z_err (ISO)]  FLOAT,
    [z (APER)]     FLOAT,
    [z_err (APER)] FLOAT,
    [W1-W2]        FLOAT,
    W1             FLOAT,
    W1_err         FLOAT,
    W2             FLOAT,
    W2_err         FLOAT,
    flag           TEXT 
);


-- Table: data_references
CREATE TABLE data_references ( 
    cluster_uid     INTEGER NOT NULL,
    reference_table TEXT    NOT NULL,
    reference_uid   TEXT    NOT NULL 
);


-- Table: data_values
CREATE TABLE data_values ( 
    cluster_uid    INT             NOT NULL
                                   REFERENCES clusters ( uid ),
    [key]          CHAR( 25 )      NOT NULL,
    key_class      CHAR( 25 ),
    source         CHAR( 25 )      NOT NULL
                                   REFERENCES data_sources ( source ),
    value          REAL,
    value_err_low  REAL,
    value_err_high REAL,
    comment        TEXT,
    external_link  VARCHAR( 300 ) 
);


-- Table: key_referencer
CREATE TABLE key_referencer ( 
    [key]             TEXT    NOT NULL,
    key_class         TEXT,
    reference_table   TEXT    NOT NULL,
    reference_column  TEXT    NOT NULL,
    is_string         INTEGER NOT NULL
                              DEFAULT 0,
    error_column_low  TEXT,
    error_column_high TEXT,
    comment           TEXT 
);


-- Table: reference_tables
CREATE TABLE reference_tables ( 
    table_name    TEXT    NOT NULL,
    uid_column    TEXT    NOT NULL,
    is_string_uid INTEGER NOT NULL
                          DEFAULT 0,
    extra_column  TEXT,
    description   TEXT 
);


-- Table: twoxmm_sources
CREATE TABLE twoxmm_sources ( 
    SRCID            INTEGER,
    IAUNAME          TEXT,
    SC_RA            DOUBLE PRECISION,
    SC_DEC           DOUBLE PRECISION,
    SC_POSERR        FLOAT,
    SC_DET_ML        FLOAT,
    SC_EP_1_FLUX     FLOAT,
    SC_EP_1_FLUX_ERR FLOAT,
    SC_EP_2_FLUX     FLOAT,
    SC_EP_2_FLUX_ERR FLOAT,
    SC_EP_3_FLUX     FLOAT,
    SC_EP_3_FLUX_ERR FLOAT,
    SC_EP_4_FLUX     FLOAT,
    SC_EP_4_FLUX_ERR FLOAT,
    SC_EP_5_FLUX     FLOAT,
    SC_EP_5_FLUX_ERR FLOAT,
    SC_EP_8_FLUX     FLOAT,
    SC_EP_8_FLUX_ERR FLOAT,
    SC_EP_9_FLUX     FLOAT,
    SC_EP_9_FLUX_ERR FLOAT,
    SC_HR1           FLOAT,
    SC_HR1_ERR       FLOAT,
    SC_HR2           FLOAT,
    SC_HR2_ERR       FLOAT,
    SC_HR3           FLOAT,
    SC_HR3_ERR       FLOAT,
    SC_HR4           FLOAT,
    SC_HR4_ERR       FLOAT,
    SC_EXTENT        FLOAT,
    SC_EXT_ML        FLOAT,
    SC_CHI2PROB      FLOAT,
    SC_VAR_FLAG      BOOL,
    SC_SUM_FLAG      INTEGER,
    N_DETECTIONS     INTEGER,
    CONFUSED         BOOL,
    SC_DR_FIRST      INTEGER,
    SC_DR_LAST       INTEGER,
    LEDAS_URL        TEXT 
);


-- Table: twoxmm_detections
CREATE TABLE twoxmm_detections ( 
    DETID            INTEGER,
    SRCID            INTEGER,
    SRCID_2XMMi      INTEGER,
    IAUNAME          TEXT,
    SRC_NUM          INTEGER,
    OBS_ID           TEXT,
    REVOLUT          TEXT,
    MJD_START        DOUBLE PRECISION,
    MJD_STOP         DOUBLE PRECISION,
    OBS_CLASS        INTEGER,
    PN_FILTER        TEXT,
    M1_FILTER        TEXT,
    M2_FILTER        TEXT,
    PN_SUBMODE       TEXT,
    M1_SUBMODE       TEXT,
    M2_SUBMODE       TEXT,
    RA               DOUBLE PRECISION,
    DEC              DOUBLE PRECISION,
    POSERR           FLOAT,
    LII              DOUBLE PRECISION,
    BII              DOUBLE PRECISION,
    RADEC_ERR        FLOAT,
    SYSERR           FLOAT,
    RA_UNC           DOUBLE PRECISION,
    DEC_UNC          DOUBLE PRECISION,
    EP_1_FLUX        FLOAT,
    EP_1_FLUX_ERR    FLOAT,
    EP_2_FLUX        FLOAT,
    EP_2_FLUX_ERR    FLOAT,
    EP_3_FLUX        FLOAT,
    EP_3_FLUX_ERR    FLOAT,
    EP_4_FLUX        FLOAT,
    EP_4_FLUX_ERR    FLOAT,
    EP_5_FLUX        FLOAT,
    EP_5_FLUX_ERR    FLOAT,
    EP_8_FLUX        FLOAT,
    EP_8_FLUX_ERR    FLOAT,
    EP_9_FLUX        FLOAT,
    EP_9_FLUX_ERR    FLOAT,
    PN_1_FLUX        FLOAT,
    PN_1_FLUX_ERR    FLOAT,
    PN_2_FLUX        FLOAT,
    PN_2_FLUX_ERR    FLOAT,
    PN_3_FLUX        FLOAT,
    PN_3_FLUX_ERR    FLOAT,
    PN_4_FLUX        FLOAT,
    PN_4_FLUX_ERR    FLOAT,
    PN_5_FLUX        FLOAT,
    PN_5_FLUX_ERR    FLOAT,
    PN_8_FLUX        FLOAT,
    PN_8_FLUX_ERR    FLOAT,
    PN_9_FLUX        FLOAT,
    PN_9_FLUX_ERR    FLOAT,
    M1_1_FLUX        FLOAT,
    M1_1_FLUX_ERR    FLOAT,
    M1_2_FLUX        FLOAT,
    M1_2_FLUX_ERR    FLOAT,
    M1_3_FLUX        FLOAT,
    M1_3_FLUX_ERR    FLOAT,
    M1_4_FLUX        FLOAT,
    M1_4_FLUX_ERR    FLOAT,
    M1_5_FLUX        FLOAT,
    M1_5_FLUX_ERR    FLOAT,
    M1_8_FLUX        FLOAT,
    M1_8_FLUX_ERR    FLOAT,
    M1_9_FLUX        FLOAT,
    M1_9_FLUX_ERR    FLOAT,
    M2_1_FLUX        FLOAT,
    M2_1_FLUX_ERR    FLOAT,
    M2_2_FLUX        FLOAT,
    M2_2_FLUX_ERR    FLOAT,
    M2_3_FLUX        FLOAT,
    M2_3_FLUX_ERR    FLOAT,
    M2_4_FLUX        FLOAT,
    M2_4_FLUX_ERR    FLOAT,
    M2_5_FLUX        FLOAT,
    M2_5_FLUX_ERR    FLOAT,
    M2_8_FLUX        FLOAT,
    M2_8_FLUX_ERR    FLOAT,
    M2_9_FLUX        FLOAT,
    M2_9_FLUX_ERR    FLOAT,
    EP_8_RATE        FLOAT,
    EP_8_RATE_ERR    FLOAT,
    EP_9_RATE        FLOAT,
    EP_9_RATE_ERR    FLOAT,
    PN_1_RATE        FLOAT,
    PN_1_RATE_ERR    FLOAT,
    PN_2_RATE        FLOAT,
    PN_2_RATE_ERR    FLOAT,
    PN_3_RATE        FLOAT,
    PN_3_RATE_ERR    FLOAT,
    PN_4_RATE        FLOAT,
    PN_4_RATE_ERR    FLOAT,
    PN_5_RATE        FLOAT,
    PN_5_RATE_ERR    FLOAT,
    PN_8_RATE        FLOAT,
    PN_8_RATE_ERR    FLOAT,
    PN_9_RATE        FLOAT,
    PN_9_RATE_ERR    FLOAT,
    M1_1_RATE        FLOAT,
    M1_1_RATE_ERR    FLOAT,
    M1_2_RATE        FLOAT,
    M1_2_RATE_ERR    FLOAT,
    M1_3_RATE        FLOAT,
    M1_3_RATE_ERR    FLOAT,
    M1_4_RATE        FLOAT,
    M1_4_RATE_ERR    FLOAT,
    M1_5_RATE        FLOAT,
    M1_5_RATE_ERR    FLOAT,
    M1_8_RATE        FLOAT,
    M1_8_RATE_ERR    FLOAT,
    M1_9_RATE        FLOAT,
    M1_9_RATE_ERR    FLOAT,
    M2_1_RATE        FLOAT,
    M2_1_RATE_ERR    FLOAT,
    M2_2_RATE        FLOAT,
    M2_2_RATE_ERR    FLOAT,
    M2_3_RATE        FLOAT,
    M2_3_RATE_ERR    FLOAT,
    M2_4_RATE        FLOAT,
    M2_4_RATE_ERR    FLOAT,
    M2_5_RATE        FLOAT,
    M2_5_RATE_ERR    FLOAT,
    M2_8_RATE        FLOAT,
    M2_8_RATE_ERR    FLOAT,
    M2_9_RATE        FLOAT,
    M2_9_RATE_ERR    FLOAT,
    EP_8_CTS         FLOAT,
    EP_8_CTS_ERR     FLOAT,
    PN_8_CTS         FLOAT,
    PN_8_CTS_ERR     FLOAT,
    M1_8_CTS         FLOAT,
    M1_8_CTS_ERR     FLOAT,
    M2_8_CTS         FLOAT,
    M2_8_CTS_ERR     FLOAT,
    EP_8_DET_ML      FLOAT,
    EP_9_DET_ML      FLOAT,
    PN_1_DET_ML      FLOAT,
    PN_2_DET_ML      FLOAT,
    PN_3_DET_ML      FLOAT,
    PN_4_DET_ML      FLOAT,
    PN_5_DET_ML      FLOAT,
    PN_8_DET_ML      FLOAT,
    PN_9_DET_ML      FLOAT,
    M1_1_DET_ML      FLOAT,
    M1_2_DET_ML      FLOAT,
    M1_3_DET_ML      FLOAT,
    M1_4_DET_ML      FLOAT,
    M1_5_DET_ML      FLOAT,
    M1_8_DET_ML      FLOAT,
    M1_9_DET_ML      FLOAT,
    M2_1_DET_ML      FLOAT,
    M2_2_DET_ML      FLOAT,
    M2_3_DET_ML      FLOAT,
    M2_4_DET_ML      FLOAT,
    M2_5_DET_ML      FLOAT,
    M2_8_DET_ML      FLOAT,
    M2_9_DET_ML      FLOAT,
    EP_EXTENT        FLOAT,
    EP_EXTENT_ERR    FLOAT,
    EP_EXTENT_ML     FLOAT,
    EP_HR1           FLOAT,
    EP_HR1_ERR       FLOAT,
    EP_HR2           FLOAT,
    EP_HR2_ERR       FLOAT,
    EP_HR3           FLOAT,
    EP_HR3_ERR       FLOAT,
    EP_HR4           FLOAT,
    EP_HR4_ERR       FLOAT,
    PN_HR1           FLOAT,
    PN_HR1_ERR       FLOAT,
    PN_HR2           FLOAT,
    PN_HR2_ERR       FLOAT,
    PN_HR3           FLOAT,
    PN_HR3_ERR       FLOAT,
    PN_HR4           FLOAT,
    PN_HR4_ERR       FLOAT,
    M1_HR1           FLOAT,
    M1_HR1_ERR       FLOAT,
    M1_HR2           FLOAT,
    M1_HR2_ERR       FLOAT,
    M1_HR3           FLOAT,
    M1_HR3_ERR       FLOAT,
    M1_HR4           FLOAT,
    M1_HR4_ERR       FLOAT,
    M2_HR1           FLOAT,
    M2_HR1_ERR       FLOAT,
    M2_HR2           FLOAT,
    M2_HR2_ERR       FLOAT,
    M2_HR3           FLOAT,
    M2_HR3_ERR       FLOAT,
    M2_HR4           FLOAT,
    M2_HR4_ERR       FLOAT,
    PN_1_EXP         FLOAT,
    PN_2_EXP         FLOAT,
    PN_3_EXP         FLOAT,
    PN_4_EXP         FLOAT,
    PN_5_EXP         FLOAT,
    M1_1_EXP         FLOAT,
    M1_2_EXP         FLOAT,
    M1_3_EXP         FLOAT,
    M1_4_EXP         FLOAT,
    M1_5_EXP         FLOAT,
    M2_1_EXP         FLOAT,
    M2_2_EXP         FLOAT,
    M2_3_EXP         FLOAT,
    M2_4_EXP         FLOAT,
    M2_5_EXP         FLOAT,
    PN_1_BG          FLOAT,
    PN_2_BG          FLOAT,
    PN_3_BG          FLOAT,
    PN_4_BG          FLOAT,
    PN_5_BG          FLOAT,
    M1_1_BG          FLOAT,
    M1_2_BG          FLOAT,
    M1_3_BG          FLOAT,
    M1_4_BG          FLOAT,
    M1_5_BG          FLOAT,
    M2_1_BG          FLOAT,
    M2_2_BG          FLOAT,
    M2_3_BG          FLOAT,
    M2_4_BG          FLOAT,
    M2_5_BG          FLOAT,
    PN_1_VIG         FLOAT,
    PN_2_VIG         FLOAT,
    PN_3_VIG         FLOAT,
    PN_4_VIG         FLOAT,
    PN_5_VIG         FLOAT,
    M1_1_VIG         FLOAT,
    M1_2_VIG         FLOAT,
    M1_3_VIG         FLOAT,
    M1_4_VIG         FLOAT,
    M1_5_VIG         FLOAT,
    M2_1_VIG         FLOAT,
    M2_2_VIG         FLOAT,
    M2_3_VIG         FLOAT,
    M2_4_VIG         FLOAT,
    M2_5_VIG         FLOAT,
    PN_ONTIME        FLOAT,
    M1_ONTIME        FLOAT,
    M2_ONTIME        FLOAT,
    EP_ONTIME        FLOAT,
    PN_OFFAX         FLOAT,
    M1_OFFAX         FLOAT,
    M2_OFFAX         FLOAT,
    EP_OFFAX         FLOAT,
    PN_MASKFRAC      FLOAT,
    M1_MASKFRAC      FLOAT,
    M2_MASKFRAC      FLOAT,
    DIST_NN          FLOAT,
    SUM_FLAG         INTEGER,
    EP_FLAG          TEXT,
    PN_FLAG          TEXT,
    M1_FLAG          TEXT,
    M2_FLAG          TEXT,
    TSERIES          BOOL,
    SPECTRA          BOOL,
    EP_CHI2PROB      FLOAT,
    PN_CHI2PROB      FLOAT,
    M1_CHI2PROB      FLOAT,
    M2_CHI2PROB      FLOAT,
    VAR_FLAG         BOOL,
    VAR_EXP_ID       TEXT,
    VAR_INST_ID      TEXT,
    SC_RA            DOUBLE PRECISION,
    SC_DEC           DOUBLE PRECISION,
    SC_POSERR        FLOAT,
    SC_DET_ML        FLOAT,
    SC_EP_1_FLUX     FLOAT,
    SC_EP_1_FLUX_ERR FLOAT,
    SC_EP_2_FLUX     FLOAT,
    SC_EP_2_FLUX_ERR FLOAT,
    SC_EP_3_FLUX     FLOAT,
    SC_EP_3_FLUX_ERR FLOAT,
    SC_EP_4_FLUX     FLOAT,
    SC_EP_4_FLUX_ERR FLOAT,
    SC_EP_5_FLUX     FLOAT,
    SC_EP_5_FLUX_ERR FLOAT,
    SC_EP_8_FLUX     FLOAT,
    SC_EP_8_FLUX_ERR FLOAT,
    SC_EP_9_FLUX     FLOAT,
    SC_EP_9_FLUX_ERR FLOAT,
    SC_HR1           FLOAT,
    SC_HR1_ERR       FLOAT,
    SC_HR2           FLOAT,
    SC_HR2_ERR       FLOAT,
    SC_HR3           FLOAT,
    SC_HR3_ERR       FLOAT,
    SC_HR4           FLOAT,
    SC_HR4_ERR       FLOAT,
    SC_EXTENT        FLOAT,
    SC_EXT_ML        FLOAT,
    SC_CHI2PROB      FLOAT,
    SC_VAR_FLAG      BOOL,
    SC_SUM_FLAG      INTEGER,
    SC_DR_FIRST      INTEGER,
    SC_DR_LAST       INTEGER,
    N_DETECTIONS     INTEGER,
    CONFUSED         BOOL 
);


-- Index: i_3xmm_detections_srcid
CREATE INDEX i_3xmm_detections_srcid ON threexmm_detections ( 
    SRCID ASC 
);


-- Index: idx_threexmm_sources
CREATE INDEX idx_threexmm_sources ON threexmm_sources ( 
    SRCID ASC 
);


-- Index: idx_threexmm_detections
CREATE INDEX idx_threexmm_detections ON threexmm_detections ( 
    DETID ASC 
);
