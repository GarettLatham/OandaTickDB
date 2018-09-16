CREATE TABLE `tick` (
 `tick_datetime` datetime NOT NULL,
 `tick_timestamp` int(10) unsigned NOT NULL,
 `tick_year` smallint(2) unsigned NOT NULL,
 `tick_hour` tinyint(2) unsigned NOT NULL,
 `tick_minute` tinyint(2) unsigned NOT NULL,
 `tick_second` tinyint(2) unsigned NOT NULL,
 `tick_dayofweek` tinyint(1) unsigned NOT NULL,
 `tick_dayofmonth` tinyint(2) unsigned NOT NULL,
 `tick_dayofyear` smallint(2) unsigned NOT NULL,
 `tick_security` varchar(7) NOT NULL,
 `tick_openMid` decimal(10,6) unsigned NOT NULL,
 `tick_highMid` decimal(10,6) unsigned NOT NULL,
 `tick_lowMid` decimal(10,6) unsigned NOT NULL,
 `tick_closeMid` decimal(10,6) unsigned NOT NULL,
 `tick_volume` int(11) unsigned NOT NULL,
 `tick_granularity` varchar(3) NOT NULL,
 PRIMARY KEY (`tick_timestamp`,`tick_security`,`tick_granularity`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
