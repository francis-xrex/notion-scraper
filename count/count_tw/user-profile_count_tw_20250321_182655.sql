SET FOREIGN_KEY_CHECKS=0;
USE user_profile;

/*
Execute check script to make sure if exist cross institution data
*/

-- check club
SELECT count(1)
FROM user_profile.club c
JOIN user_profile.club_user cu on c.id = cu.club_id
JOIN user_profile.removed_user u on cu.user_id = u.user_id
WHERE cu.user_role = 'OWNER';

-- check club application
SELECT count(1) 
FROM user_profile.club_application ca 
JOIN user_profile.removed_user u on ca.user_id = u.user_id;

-- check club user
SELECT count(1) 
FROM user_profile.club_user cu
WHERE cu.club_id NOT IN (SELECT id FROM user_profile.club) 
 OR EXISTS (SELECT 1 FROM user_profile.removed_user u WHERE cu.user_id = u.user_id);

-- check club user volume
SELECT count(1) 
FROM user_profile.club_user_volume cuv
WHERE cuv.club_user_id NOT IN (SELECT id FROM user_profile.club_user);

-- check club volume level
SELECT count(1) 
FROM user_profile.club_volume_level cvl 
WHERE cvl.club_id NOT IN (SELECT id FROM user_profile.club);

-- check user contact
SELECT count(1) FROM user_profile.contact
WHERE EXISTS (
 SELECT 1 FROM user_profile.removed_user u
 WHERE user_profile.contact.user_id = u.user_id
 OR user_profile.contact.friend_user_id = u.user_id
);

-- check user_recent_interaction_record
SELECT count(1) FROM user_profile.user_recent_interaction_record
WHERE EXISTS (
 SELECT 1 FROM user_profile.removed_user u
 WHERE user_profile.user_recent_interaction_record.user_id = u.user_id
 OR user_profile.user_recent_interaction_record.friend_user_id = u.user_id
);

SELECT count(1) FROM user_profile.admin_operation_log_for_user a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

SELECT count(1) FROM user_profile.history_login a 
JOIN user_profile.removed_user u ON u.chainup_id = a.uid;

SELECT count(1) FROM user_profile.history_setting a 
JOIN user_profile.removed_user u ON u.chainup_id = a.uid;

SELECT count(1) FROM user_profile.user a 
JOIN user_profile.removed_user u ON u.chainup_id = a.id;

SELECT count(1) FROM user_profile.user_belong a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

SELECT count(1) FROM user_profile.user_default_file_setting a 
JOIN user_profile.removed_user u ON u.user_id = a.user_id;

SELECT count(1) FROM user_profile.user_event_log a 
JOIN user_profile.removed_user u ON u.chainup_id = a.uid;

SELECT count(1) FROM user_profile.user_ext a 
JOIN user_profile.removed_user u ON u.chainup_id = a.uid;

SELECT count(1) FROM user_profile.user_file a 
JOIN user_profile.removed_user u ON u.user_id = a.user_id;

SELECT count(1) FROM user_profile.user_instruction_record a 
JOIN user_profile.removed_user u ON u.chainup_id = a.uid;

SELECT count(1) FROM user_profile.user_kyc_data a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

SELECT count(1) FROM user_profile.user_kyc_limit_vip a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

SELECT count(1) FROM user_profile.user_kyc_state a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

SELECT count(1) FROM user_profile.user_label a 
JOIN user_profile.removed_user u ON u.chainup_id = a.uid;

SELECT count(1) FROM user_profile.user_message a 
JOIN user_profile.removed_user u ON u.chainup_id = a.receive_uid;

SELECT count(1) FROM user_profile.user_platform_info a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

SELECT count(1) FROM user_profile.user_private_note a 
JOIN user_profile.removed_user u ON u.user_id = a.user_id;

SELECT count(1) FROM user_profile.user_volume_level a 
JOIN user_profile.removed_user u ON u.user_id = a.user_id;

SELECT count(1) FROM user_profile.user_whitelist a 
JOIN user_profile.removed_user u ON u.user_id = a.user_id;