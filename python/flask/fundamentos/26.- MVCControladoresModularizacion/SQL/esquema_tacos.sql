-- ==========================================================
-- ESQUEMA DE BASE DE DATOS
-- ==========================================================

CREATE SCHEMA IF NOT EXISTS
    `esquema_tacos`
    DEFAULT CHARACTER SET utf8;


USE `esquema_tacos`;


-- ==========================================================
-- TABLA TACOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS `tacos` (

    `id` INT NOT NULL AUTO_INCREMENT,

    `tortilla` VARCHAR(45) NULL,

    `guiso` VARCHAR(45) NULL,

    `salsa` VARCHAR(45) NULL,

    `created_at`
        DATETIME NULL
        DEFAULT CURRENT_TIMESTAMP,

    `updated_at`
        DATETIME NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`)

) ENGINE = InnoDB;