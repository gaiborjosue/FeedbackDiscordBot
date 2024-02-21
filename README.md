# Feedback Wizard Bot

Feedback Wizard Bot is a Discord bot designed to enhance the feedback and grading process within educational or training-oriented Discord servers. It simplifies the distribution and management of assignment feedback and grade distributions.

```
   ___             _ _                _      __    __ _                  _ 
  / __\__  ___  __| | |__   __ _  ___| | __ / / /\ \ (_)______ _ _ __ __| |
 / _\/ _ \/ _ \/ _` | '_ \ / _` |/ __| |/ / \ \/  \/ / |_  / _` | '__/ _` |
/ / |  __/  __/ (_| | |_) | (_| | (__|   <   \  /\  /| |/ / (_| | | | (_| |
\/   \___|\___|\__,_|_.__/ \__,_|\___|_|\_\   \/  \/ |_/___\__,_|_|  \__,_|
                                                                           
                                      ....
                                .'' .'''
.                             .'   :
\\                          .:    :
 \\                        _:    :       ..----.._
  \\                    .:::.....:::.. .'         ''.
   \\                 .'  #-. .-######'     #        '.
    \\                 '.##'/ ' ################       :
     \\                  #####################         :
      \\               ..##.-.#### .''''###'.._        :
       \\             :--:########:            '.    .' :
        \\..__...--.. :--:#######.'   '.         '.     :
        :     :  : : '':'-:'':'::        .         '.  .'
        '---'''..: :    ':    '..'''.      '.        :'
           \\  :: : :     '      ''''''.     '.      .:
            \\ ::  : :     '            '.      '      :
             \\::   : :           ....' ..:       '     '.
              \\::  : :    .....####\\ .~~.:.             :
               \\':.:.:.:'#########.===. ~ |.'-.   . '''.. :
                \\    .'  ########## \ \ _.' '. '-.       '''.
                :\\  :     ########   \ \      '.  '-.        :
               :  \\'    '   #### :    \ \      :.    '-.      :
              :  .'\\   :'  :     :     \ \       :      '-.    :
             : .'  .\\  '  :      :     :\ \       :        '.   :
             ::   :  \\'  :.      :     : \ \      :          '. :
             ::. :    \\  : :      :    ;  \ \     :           '.:
              : ':    '\\ :  :     :     :  \:\     :        ..'
                 :    ' \\ :        :     ;  \|      :   .'''
                 '.   '  \\:                         :.''
                  .:..... \\:       :            ..''
                 '._____|'.\\......'''''''.:..'''
```
## Getting Started

### Invite the Bot to Your Server

You can invite Feedback Wizard Bot to your Discord server using the following link:

[Invite Feedback Wizard Bot](https://discord.com/api/oauth2/authorize?client_id=1209653579879555122&permissions=8&scope=bot)

### Discord Server Configuration

For the bot to function properly, your server needs to have two specific channels:

- **_staff**: A channel dedicated to staff members for managing feedback and grades. This channel should only be accessible to staff members and the bot.
- **feedback**: A channel where students can request and receive feedback. This channel should be accessible to both staff and students.

## Commands

Feedback Wizard Bot provides a set of commands for staff and students to interact with the feedback system efficiently.

### Staff Commands

- `!newfeedback <assignment_number> <feedback_url>`: Add a new feedback link for an assignment.
- `!summary <assignment_number> [background_color] [bar_color] [label_color]`: Generate and share a bar graph showing the grade distribution for an assignment. The colors are optional parameters for customization.
- `!feedbacklink <assignment_number>`: Retrieve and share the feedback link for a specific assignment.
- `!feedbacklist`: List all available feedback links for assignments.
- `!deletefeedback <assignment_number>`: Delete a feedback link for a specific assignment.
- `!helpstaff`: Display detailed help for all staff commands.

### Student Commands

- `!feedback [assignment_number]`: Students can request feedback for a specific assignment. If the assignment number is omitted, the bot will provide feedback for the most recent assignment.
- `!helpstudent`: Display detailed help for all student commands.

## Functionalities
### Dynamic Feedback Banner Design

- The bot customizes the feedback message banner sent to students based on the server from which the request originated.
- For servers on the bot's known list, it sends feedback with a custom banner design that aligns with the server's theme or branding.
- For all other servers, the bot sends feedback with a default banner design. This ensures that even if the server isn't on the known list, students still receive their feedback in a visually appealing format.
- **To request your server to be added to the known list with a custom banner, please create an issue on this repo :)**

### Server-specific Assignment Management

- Feedback Wizard Bot manages assignment URLs on a per-server basis. This means that each server can have its own set of assignments and feedback links, independent of other servers.
- This functionality allows for tailored assignment management and feedback distribution, ensuring that the information remains relevant and organized according to each server's specific needs and structure.

## Support

For support, questions, or contributions, please open an issue :)

## License

This project is licensed under the MIT License
