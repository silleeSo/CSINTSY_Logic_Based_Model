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

% Rules for recommending partner based on MBTI
recommend_partner(MBTI, Partner) :- compatible(MBTI, Partner).

% Rules for recommending attachment style based on MBTI
recommend_attachment_style(intj, avoidant).
recommend_attachment_style(entp, secure).
recommend_attachment_style(infj, anxious).
recommend_attachment_style(enfp, anxious).
recommend_attachment_style(isfj, secure).
recommend_attachment_style(estj, secure).
recommend_attachment_style(esfp, secure).
recommend_attachment_style(istp, avoidant).
recommend_attachment_style(intp, avoidant).
recommend_attachment_style(entj, secure).
recommend_attachment_style(infp, anxious).
recommend_attachment_style(enfj, secure).
recommend_attachment_style(istj, secure).
recommend_attachment_style(isfp, anxious).
recommend_attachment_style(estp, secure).
recommend_attachment_style(esfj, secure).

% Rules for recommending communication style based on MBTI
recommend_communication_style(intj, assertive).
recommend_communication_style(entp, assertive).
recommend_communication_style(infj, passive).
recommend_communication_style(enfp, assertive).
recommend_communication_style(isfj, passive).
recommend_communication_style(estj, assertive).
recommend_communication_style(esfp, assertive).
recommend_communication_style(istp, assertive).
recommend_communication_style(intp, passive).
recommend_communication_style(entj, assertive).
recommend_communication_style(infp, passive).
recommend_communication_style(enfj, assertive).
recommend_communication_style(istj, assertive).
recommend_communication_style(isfp, passive).
recommend_communication_style(estp, assertive).
recommend_communication_style(esfj, assertive).

% Rules for recommending love language based on MBTI
recommend_love_language(intj, acts_of_service).
recommend_love_language(entp, words_of_affirmation).
recommend_love_language(infj, quality_time).
recommend_love_language(enfp, words_of_affirmation).
recommend_love_language(isfj, acts_of_service).
recommend_love_language(estj, acts_of_service).
recommend_love_language(esfp, physical_touch).
recommend_love_language(istp, physical_touch).
recommend_love_language(intp, quality_time).
recommend_love_language(entj, acts_of_service).
recommend_love_language(infp, words_of_affirmation).
recommend_love_language(enfj, quality_time).
recommend_love_language(istj, acts_of_service).
recommend_love_language(isfp, physical_touch).
recommend_love_language(estp, physical_touch).
recommend_love_language(esfj, words_of_affirmation).

% Rules for recommending interest
recommend_interest(Interest, PartnerInterest) :- interest(Interest), interest(PartnerInterest).

% Rules for recommending values
recommend_value(Value, PartnerValue) :- value(Value), value(PartnerValue).

% Interactive session with the user
start :-
    write('Welcome to the Relationship Advisor Expert System!'), nl,
    prompt_user(mbti, UserMBTI),
    recommend_attachment_style(UserMBTI, UserAttachmentStyle),
    format('Based on your MBTI, your attachment style is: ~w', [UserAttachmentStyle]), nl,
    recommend_communication_style(UserMBTI, UserCommunicationStyle),
    format('Based on your MBTI, your communication style is: ~w', [UserCommunicationStyle]), nl,
    recommend_love_language(UserMBTI, UserLoveLanguage),
    format('Based on your MBTI, your love language is: ~w', [UserLoveLanguage]), nl,
    prompt_user(interest, UserInterest),
    prompt_user(value, UserValue),
    recommend(UserMBTI, UserAttachmentStyle, UserLoveLanguage, UserInterest, UserValue, UserCommunicationStyle).

prompt_user(Type, UserInput) :-
    format('Please enter your ~w (', [Type]),
    findall(X, call(Type, X), List),
    format_list(List),
    write('): '), nl,
    read_line_to_codes(user_input, Codes),
    atom_codes(InputAtom, Codes),
    (call(Type, InputAtom) -> UserInput = InputAtom ; write('Invalid input. Please try again.'), nl, prompt_user(Type, UserInput)).

format_list([Last]) :- !, write(Last).
format_list([Head|Tail]) :- write(Head), write(', '), format_list(Tail).

recommend(UserMBTI, UserAttachmentStyle, UserLoveLanguage, UserInterest, UserValue, UserCommunicationStyle) :-
    recommend_partner(UserMBTI, Partner),
    format('Your recommended partner MBTI type is: ~w', [Partner]), nl,
    recommend_interest(UserInterest, InterestRecommendation),
    format('Your recommended interest match is: ~w', [InterestRecommendation]), nl,
    recommend_value(UserValue, ValueRecommendation),
    format('Your recommended value match is: ~w', [ValueRecommendation]), nl,
    format('Your recommended attachment style match is: ~w', [UserAttachmentStyle]), nl,
    format('Your recommended communication style match is: ~w', [UserCommunicationStyle]), nl,
    format('Your recommended love language match is: ~w', [UserLoveLanguage]), nl.

% Run the program
:- start.
