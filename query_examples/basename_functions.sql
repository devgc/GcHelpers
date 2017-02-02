SELECT
'Partition 1\TEST_P1 [NTFS]\[root]\testfolder002\testfolder001\testfile088.png' AS "Filename 1",
Basename(
	'Partition 1\TEST_P1 [NTFS]\[root]\testfolder002\testfolder001\testfile088.png'
) AS "Filename 2",
BasenameN(
	'Partition 1\TEST_P1 [NTFS]\[root]\testfolder002\testfolder001\testfile088.png',
	1
) AS "Filename 3"