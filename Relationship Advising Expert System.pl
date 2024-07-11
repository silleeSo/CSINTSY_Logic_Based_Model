% Facts about MBTI types
mbti(intj).
mbti(entp).
mbti(infj).
mbti(enfp).
mbti(isfj).
mbti(estj).
mbti(esfp).
mbti(istp).

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

% Facts about values
value(family).
value(career).
value(friends).
value(personal_growth).

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

% Rules for recommending communication style based on MBTI
recommend_communication_style(intj, assertive).
recommend_communication_style(entp, aggressive).
recommend_communication_style(infj, passive).
recommend_communication_style(enfp, passive_aggressive).
recommend_communication_style(isfj, passive).
recommend_communication_style(estj, assertive).
recommend_communication_style(esfp, passive_aggressive).
recommend_communication_style(istp, passive).

% Rules for recommending love language
recommend_love_language(words_of_affirmation, quality_time).
recommend_love_language(acts_of_service, receiving_gifts).
recommend_love_language(receiving_gifts, physical_touch).
recommend_love_language(quality_time, words_of_affirmation).
recommend_love_language(physical_touch, acts_of_service).

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
    prompt_user(love_language, UserLoveLanguage),
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
    recommend_love_language(UserLoveLanguage, LoveLanguageRecommendation),
    format('Your recommended love language match is: ~w', [LoveLanguageRecommendation]), nl,
    recommend_interest(UserInterest, InterestRecommendation),
    format('Your recommended interest match is: ~w', [InterestRecommendation]), nl,
    recommend_value(UserValue, ValueRecommendation),
    format('Your recommended value match is: ~w', [ValueRecommendation]), nl,
    format('Your recommended attachment style match is: ~w', [UserAttachmentStyle]), nl,
    format('Your recommended communication style match is: ~w', [UserCommunicationStyle]), nl.

% Run the program
:- start.
