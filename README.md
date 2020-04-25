# ECE-356-Project
BY:

Sean He 20662918 

Chengang Sun 20658073


## Functions:

### signup
Prompts the user for an alias (unique), password, email, gender, occupation, birthDate (non empty). Then insers a user into the user table with the given data.

User must be logged out to use.

### login
Prompts the user for their username/alias and password. Verifies that password is correct and saves userID to the client on success. This ID will determine who is logged on.

User must be logged out to use.

### logout
Frees the userID from the client.

User must be logged in to use.

### create_group
Prompts the user for a groupName for the new group. Verifies that this name is unique. If succeeds inserts a new entry to the UserGroups table and inserts the creator as a member of the new group into the Members table.

User must be logged in to use.

### join_group
Prompts the user for a groupName and role. If the group exists, will insert and entry into the Members table adding the user to the group with the given role

User must be logged in to use.

### get_my_groups
Outputs all groups that the use is part of and the role the user has in the group.

User must be logged in to use.

### quit_group
Prompts the user for a group name. If the group exists and the user is part of the group then delete the entry causing the user to be removed from the group.

User must be logged in to use.

### delete_group
Prompts the user for a group name. If the group exists and the user is the one who created the group then remove all member of the group and delete the group.

User must be logged in to use.

### topics
Returns all root topics. Prompts user to input a topic name (on screen) and will output its children. This process is continued until the leaf topic is reached.

User must be logged in to use.

### create_post
Prompts the user for a topic name, post content, image (optional) and link (optional). It will then search for the topic, if it doesnt exist it will create a new root topic (no parents). Inserts an entry into Posts table with respective information and will insert respective data into Images and Links tables if the info is provided.

User must be logged in to use.

### create_reply
Same as create_post except user will be prompted to insert a post id as well. This will link to the parent post that is being replies to.

User must be logged in to use.

### get_single_post
Prompts the user for a post id. Will serach for the post, If it exists, will return all relevant information of the post. Updates Seen table.

User must be logged in to use.

### get_topic_posts
Prompts the user for a topic name. Will search for all subtopics of the topic (however many levels deep) and return all posts in those topics. Updates Seen table.

User must be logged in to use.

### get_user_posts
Promps the user for a username/alias. Will return all posts from the target user. Updates Seen table.

User must be logged in to use.

### get_new_posts
Returns all the unseen posts the current user is following. From followed Users and Topics (includes subtopics). Updates Seen table.

User must be logged in to use.

### thumb_up
Upserts into ThumbsUpDown table with a thumbs up.

User must be logged in to use.

### thumb_down
Upserts into ThumbsUpDown table with a thumbs down.

User must be logged in to use.

### follow
Prompts user to follow a user or topic. If input is valid it will update FollowsUser or FollowsTopic table accordingly.

User must be logged in to use.

### unfollow
Prompts user to unfollow a user or topic. If input is valid it will delete entry from FollowsUser or FollowsTopic table accordingly.

User must be logged in to use.

### get_follows
Outputs all users and Topics the user is currently following.

User must be logged in to use.

               
