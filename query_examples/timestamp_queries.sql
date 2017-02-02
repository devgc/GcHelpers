SELECT
"2017-Jan-11 15:16:27.467916 UTC" AS "Timestamp 1",
DtFormat(
	'2017-Jan-11 15:16:27.467916 UTC',
	'{0.year:04d}-{0.month:02d}-{0.day:02d} {0.hour:02d}:{0.minute:02d}:{0.second:02d}.{0.microsecond:06d}'
) AS "Timestamp 2",
DtFormatTz(
	'2017-Jan-11 15:16:27.467916 UTC',
	'{0.year:04d}-{0.month:02d}-{0.day:02d} {0.hour:02d}:{0.minute:02d}:{0.second:02d}.{0.microsecond:06d}',
	'UTC',
	'America/Chicago'
) AS "Timestamp 3"