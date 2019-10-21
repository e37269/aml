CREATE TABLE `aml` (
	`ise_id` VARCHAR(25) NOT NULL COLLATE 'latin1_german1_ci',
	`status` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`number` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`emergency_number` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_latitude` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_longitude` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_time` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_altitude` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_floor` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_source` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_accuracy` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_vertical_accuracy` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_confidence` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_bearing` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`location_speed` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`aml_json` VARCHAR(2500) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	`anrufzeit` VARCHAR(25) NULL DEFAULT NULL COLLATE 'latin1_german2_ci',
	PRIMARY KEY (`ise_id`)
)
COLLATE='latin1_german2_ci'
ENGINE=MyISAM
;