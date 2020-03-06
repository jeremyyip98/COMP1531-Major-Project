### Assumptions

- Assume that when called channel_list_all should list all channels including id and name regardless if the user is in the channel or not, compared to channel list which only list the channels the user is in.

- Assume that owners are also in the member list

- Assume that when you add someone to a channel they are already apart of would raise an input error like add_owner

- Assume a channel can have 0 members 

- Assume all user made are not admins

- Assume tokens are unique between users and there is only one token per user per session

- Assume channel_invite InputError: "channel_id does not refer to a valid channel that the authorised user is part of." refers to the channel having an invalid channel_id AND the AccessError: "the authorised user is not already a member of the channel" as being when the authorised user is not a member of the channel but invites another user to the channel

- Assumed that maximum password length is 50 characters

- Assumed that "hopefullythisisnotavalidtoken" is not a valid token

- Assume register and login functions always return a valid token

- Assume that users_all lists users in order of when they registered 

- Assume that logging out with an invalid token throws access error instead of "is_success" = True

- Assume that logging out a logged out user with a valid token returns "is_success" = False


---

![alt text](https://m.media-amazon.com/images/M/MV5BOTFmYTc3ZWEtNTYxNi00OTA4LTk2NjEtNTI2MTJlNzkyMDdlXkEyXkFqcGdeQWpybA@@._V1_UX477_CR0,0,477,268_AL_.jpg)
            *Not our image*   

