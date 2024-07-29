% Facts about MBTI types
mbti(intj).
mbti(entp).
mbti(infj).
mbti(enfp).
mbti(isfj).
mbti(estj).
mbti(esfp).
mbti(istp).
mbti(intp).
mbti(entj).
mbti(infp).
mbti(enfj).
mbti(istj).
mbti(isfp).
mbti(estp).
mbti(esfj).

% Facts about attachment styles
attachment_style(secure).
attachment_style(anxious).
attachment_style(avoidant).
attachment_style(fearful_avoidant).

% Facts about love languages
love_language(words_of_affirmation).
love_language(acts_of_service).
love_language(receiving_gifts).
love_language(quality_time).
love_language(physical_touch).

% Facts about interests
interest(reading).
interest(traveling).
interest(sports).
interest(music).
interest(cooking).
interest(art).
interest(gaming).
interest(hiking).

% Facts about values
value(family).
value(career).
value(friends).
value(personal_growth).
value(adventure).
value(stability).
value(independence).
value(community).

% Facts about communication styles
communication_style(assertive).
communication_style(passive).
communication_style(aggressive).
communication_style(passive_aggressive).

% Facts about MBTI compatibility
compatible(intj, entp).
compatible(entp, intj).
compatible(infj, enfp).
compatible(enfp, infj).
compatible(isfj, estj).
compatible(estj, isfj).
compatible(esfp, istp).
compatible(istp, esfp).
compatible(intp, enfj).
compatible(entj, infp).
compatible(infp, enfj).
compatible(enfj, intp).
compatible(istj, esfj).
compatible(isfp, estp).
compatible(estp, isfp).
compatible(esfj, istj).



% Facts for recommending attachment style based on MBTI
possible_attachment_style(intj, avoidant).
possible_attachment_style(entp, secure).
possible_attachment_style(infj, anxious).
possible_attachment_style(enfp, anxious).
possible_attachment_style(isfj, secure).
possible_attachment_style(estj, secure).
possible_attachment_style(esfp, secure).
possible_attachment_style(istp, avoidant).
possible_attachment_style(intp, avoidant).
possible_attachment_style(entj, secure).
possible_attachment_style(infp, anxious).
possible_attachment_style(enfj, secure).
possible_attachment_style(istj, secure).
possible_attachment_style(isfp, anxious).
possible_attachment_style(estp, secure).
possible_attachment_style(esfj, secure).

% Rules for recommending communication style based on MBTI
possible_communication_style(entp, assertive).
possible_communication_style(infj, passive).
possible_communication_style(enfp, assertive).
possible_communication_style(isfj, passive).
possible_communication_style(estj, assertive).
possible_communication_style(esfp, assertive).
possible_communication_style(istp, assertive).
possible_communication_style(intp, passive).
possible_communication_style(entj, assertive).
possible_communication_style(infp, passive).
possible_communication_style(enfj, assertive).
possible_communication_style(istj, assertive).
possible_communication_style(isfp, passive).
possible_communication_style(estp, assertive).
possible_communication_style(esfj, assertive).



% Facts for complementing love language
complementing_love_language(acts_of_service, receiving_gifts).
complementing_love_language(receiving_gifts, acts_of_service).
complementing_love_language(words_of_affirmation, quality_time).
complementing_love_language(quality_time, words_of_affirmation).
complementing_love_language(physical_touch, quality_time).

% Facts about values complements
complementing_value(independence, personal_growth).
complementing_value(personal_growth, independence).
complementing_value(friends, family).
complementing_value(family, friends).
complementing_value(community, career).
complementing_value(career, community).

% Facts about interests complements
complementing_interest(reading, cooking).
complementing_interest(cooking, reading).
complementing_interest(sports, gaming).
complementing_interest(gaming, sports).
complementing_interest(music, art).
complementing_interest(art, music).
complementing_interest(traveling, pet_care).
complementing_interest(pet_care, traveling).
complementing_interest(writing, science).
complementing_interest(science, writing).

% Rules 
recommended_partner(MBTI, Partner) :- compatible(MBTI, Partner).
recommended_attachment_style(MBTI, AttachmentStyle) :- possible_attachment_style(MBTI, AttachmentStyle).
recommended_communication_style(MBTI, CommunicationStyle) :- possible_communication_style(MBTI, CommunicationStyle).
recommended_partner_love_language(LoveLanguage, PartnerLoveLanguage) :- complementing_love_language(LoveLanguage, PartnerLoveLanguage).
recommended_partner_value(Value, PartnerValue) :- complementing_value(Value, PartnerValue).
recommended_partner_interest(Interest, PartnerInterest) :- complementing_interest(Interest, PartnerInterest).
