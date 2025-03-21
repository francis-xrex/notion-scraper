DELETE a FROM mkyc.applicant_mobile a 
JOIN mkyc.applicant ma on a.applicant_id = ma.id
JOIN user_profile.removed_user u ON u.chainup_id = ma.chainup_id;

DELETE a FROM mkyc.applicant_institution_kyc_history a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.applicant_institution_kyc_label a
JOIN mkyc.applicant_institution_kyc aik ON a.applicant_institution_kyc_id = aik.id  
JOIN user_profile.removed_user u ON u.chainup_id = aik.chainup_id;

DELETE a FROM mkyc.applicant_kyc_document a
JOIN mkyc.applicant_kyc ak ON a.applicant_kyc_id = ak.id
JOIN mkyc.applicant ap ON ak.applicant_id = ap.id
JOIN user_profile.removed_user u ON u.chainup_id = ap.chainup_id;

DELETE a FROM mkyc.applicant_kyc_identity_review a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

-- This should retain the order
DELETE a FROM mkyc.applicant_name_screening_result a 
JOIN mkyc.applicant_name_screening_request request ON a.request_id = request.id
JOIN user_profile.removed_user u ON u.chainup_id = request.chainup_id;

DELETE a FROM mkyc.applicant_name_screening_request a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;
-- 

DELETE a FROM mkyc.applicant_threat_result a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

-- This should retain the order
DELETE item FROM mkyc.auto_review_task_item item 
JOIN mkyc.auto_review_task task ON item.task_id= task.id
JOIN mkyc.applicant_institution_kyc aik ON aik.id = task.applicant_institution_kyc_id
JOIN user_profile.removed_user u ON u.chainup_id = aik.chainup_id;

DELETE a FROM mkyc.auto_review_task a 
JOIN mkyc.applicant_institution_kyc aik ON aik.id = a.applicant_institution_kyc_id
JOIN user_profile.removed_user u ON u.chainup_id = aik.chainup_id;
-- 

DELETE a FROM mkyc.chainup_kyc_sync_result a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.conversation a 
JOIN mkyc.applicant ap ON a.applicant_id = ap.id
JOIN user_profile.removed_user u ON u.chainup_id = ap.chainup_id;

DELETE a FROM mkyc.corporate_data_history a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id

DELETE a FROM mkyc.corporate_data a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.document a
JOIN mkyc.applicant ap ON a.applicant_id = ap.id
JOIN user_profile.removed_user u ON u.chainup_id = ap.chainup_id;

DELETE a FROM mkyc.kyc3_migration_aml_case a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.personal_data_history a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.personal_data a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.user_provided_personal_data a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.vendor_twid_request a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.user_mapping a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.applicant_kyc a 
JOIN mkyc.applicant ap ON a.applicant_id = ap.id
JOIN user_profile.removed_user u ON u.chainup_id = ap.chainup_id

DELETE a FROM mkyc.applicant_institution_kyc a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;

DELETE a FROM mkyc.applicant a 
JOIN user_profile.removed_user u ON u.chainup_id = a.chainup_id;