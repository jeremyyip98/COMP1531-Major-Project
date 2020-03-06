#when called channel_list_all should list all channels including id and name regardless if the user is in the channel or not, compared to channel list which only list the channels the user is in.

#assume that owners are also in the member list

#assume that when you add someone to a channel they are already apart of would raise an input error like add_owner

#assume a channel can have 0 members 

#assume all user made are not admins

#assume tokens are unique between users and there is only one token per user per session

#assume channel_invite InputError: "channel_id does not refer to a valid channel that the authorised user is part of." refers to the channel having an invalid channel_id AND the AccessError: "the authorised user is not already a member of the channel" as being when the authorised user is not a member of the channel but invites another user to the channel
