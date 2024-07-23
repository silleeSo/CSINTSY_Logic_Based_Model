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
ideal_attachment_style(intj, avoidant).
ideal_attachment_style(entp, secure).
ideal_attachment_style(infj, anxious).
ideal_attachment_style(enfp, anxious).
ideal_attachment_style(isfj, secure).
ideal_attachment_style(estj, secure).
ideal_attachment_style(esfp, secure).
ideal_attachment_style(istp, avoidant).
ideal_attachment_style(intp, avoidant).
ideal_attachment_style(entj, secure).
ideal_attachment_style(infp, anxious).
ideal_attachment_style(enfj, secure).
ideal_attachment_style(istj, secure).
ideal_attachment_style(isfp, anxious).
ideal_attachment_style(estp, secure).
ideal_attachment_style(esfj, secure).

% Rules for recommending communication style based on MBTI
ideal_communication_style(intj, assertive).
ideal_communication_style(entp, assertive).
ideal_communication_style(infj, passive).
ideal_communication_style(enfp, assertive).
ideal_communication_style(isfj, passive).
ideal_communication_style(estj, assertive).
ideal_communication_style(esfp, assertive).
ideal_communication_style(istp, assertive).
ideal_communication_style(intp, passive).
ideal_communication_style(entj, assertive).
ideal_communication_style(infp, passive).
ideal_communication_style(enfj, assertive).
ideal_communication_style(istj, assertive).
ideal_communication_style(isfp, passive).
ideal_communication_style(estp, assertive).
ideal_communication_style(esfj, assertive).

% Facts for recommending love language based on MBTI
ideal_love_language(intj, acts_of_service).
ideal_love_language(entp, words_of_affirmation).
ideal_love_language(infj, quality_time).
ideal_love_language(enfp, words_of_affirmation).
ideal_love_language(isfj, acts_of_service).
ideal_love_language(estj, acts_of_service).
ideal_love_language(esfp, physical_touch).
ideal_love_language(istp, physical_touch).
ideal_love_language(intp, quality_time).
ideal_love_language(entj, acts_of_service).
ideal_love_language(infp, words_of_affirmation).
ideal_love_language(enfj, quality_time).
ideal_love_language(istj, acts_of_service).
ideal_love_language(isfp, physical_touch).
ideal_love_language(estp, physical_touch).
ideal_love_language(esfj, words_of_affirmation).

% Rules 
recommended_partner(MBTI, Partner) :- compatible(MBTI, Partner).
recommended_attachment_style(MBTI, AttachmentStyle) :- ideal_attachment_style(MBTI, AttachmentStyle)
recommended_communication_style(MBTI, CommunicationStyle) :- ideal_communication_style(MBTI, CommunicationStyle)
recommended_love_language(MBTI, LoveLanguage) :- ideal_love_language(MBTI, LoveLanguage)
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
    rank_values(UserValues),
    prompt_top_interests(UserInterests),
    recommend(UserMBTI, UserAttachmentStyle, UserLoveLanguage, UserInterests, UserValues, UserCommunicationStyle).

% Prompt user for MBTI
prompt_user(Type, UserInput) :-
    format('Please enter your ~w (', [Type]),
    findall(X, call(Type, X), List),
    format_list(List),
    write('): '), nl,
    read_line_to_string(user_input, InputString),
    atom_string(InputAtom, InputString),
    (call(Type, InputAtom) -> UserInput = InputAtom ; write('Invalid input. Please try again.'), nl, prompt_user(Type, UserInput)).

% Format list for displaying options
format_list([Last]) :- !, write(Last).
format_list([Head|Tail]) :- write(Head), write(', '), format_list(Tail).

% Rank values from 1 to 8
rank_values(UserValues) :-
    write('Please rank the following values from 1 to 8:'), nl,
    findall(Value, value(Value), Values),
    rank_values_list(Values, UserValues).

rank_values_list([], []).
rank_values_list([Value|Rest], [Value-Rank|UserValues]) :-
    format('Rank for ~w: ', [Value]),
    read_line_to_string(user_input, RankString),
    atom_number(RankString, Rank),
    rank_values_list(Rest, UserValues).

% Prompt user for top 3 interests
prompt_top_interests(UserInterests) :-
    write('Please select your top 3 interests from the following:'), nl,
    findall(Interest, interest(Interest), Interests),
    format_list(Interests), nl,
    select_top_interests(3, [], UserInterests).

select_top_interests(0, Selected, Selected) :- !.
select_top_interests(N, Selected, UserInterests) :-
    format('Select interest ~w: ', [N]),
    read_line_to_string(user_input, InterestString),
    atom_string(Interest, InterestString),
    (interest(Interest), \+ member(Interest, Selected) ->
        N1 is N - 1,
        select_top_interests(N1, [Interest|Selected], UserInterests)
    ;
        write('Invalid or duplicate interest. Please try again.'), nl,
        select_top_interests(N, Selected, UserInterests)
    ).

% Recommendation based on user's inputs
recommend(UserMBTI, UserAttachmentStyle, UserLoveLanguage, UserInterests, UserValues, UserCommunicationStyle) :-
    recommend_partner(UserMBTI, Partner),
    format('Your recommended partner MBTI type is: ~w', [Partner]), nl,
    recommend_top_interests(UserInterests, InterestRecommendations),
    format('Your recommended interest matches are: ~w', [InterestRecommendations]), nl,
    recommend_top_values(UserValues, ValueRecommendations),
    format('Your recommended value matches are: ~w', [ValueRecommendations]), nl,
    format('Your recommended attachment style match is: ~w', [UserAttachmentStyle]), nl,
    format('Your recommended communication style match is: ~w', [UserCommunicationStyle]), nl,
    format('Your recommended love language match is: ~w', [UserLoveLanguage]), nl.

% Recommend top 3 interests
recommend_top_interests(UserInterests, Recommendations) :-
    length(UserInterests, Length),
    (Length >= 3 ->
        findall(X, (member(X, UserInterests)), RecommendationsList),
        length(Recommendations, 3),
        append(Recommendations, _, RecommendationsList)
    ;
        Recommendations = UserInterests).

% Recommend top 3 values based on ranking
recommend_top_values(UserValues, Recommendations) :-
    sort(2, @=<, UserValues, SortedValues),
    top_n(SortedValues, 3, Recommendations).

top_n(_, 0, []) :- !.
top_n([Value-_|Rest], N, [Value|Recommendations]) :-
    N1 is N - 1,
    top_n(Rest, N1, Recommendations).

% Run the program
:- start.