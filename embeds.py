from discord import Embed, Colour

def get_embed(type):
    embed = Embed(title='AxieGlobal Admin Message', colour=Colour.from_rgb(3,178,248))
    embed.set_author(name='AxieGlobal', url='https://axieglobal.io/', icon_url='https://axieglobal-public.s3.ap-southeast-1.amazonaws.com/ag.png')
    if type == "help":
        embed.add_field(name="AxieGlobal Admin Help", value="For more info about a `Command` type **!help (command)**\n For more info about a `Category` type **!help (category)**", inline=False)
    else:
        embed.add_field(name='Automated Message - No Reply', value=get_content(type))

    return embed

def get_content(type):
    content = ""
    if type == "welcome":
        content="""Welcome to AxieGlobal!

AxieGlobal is committed to building the optimal experience for a community of players and investors in Axie Infinity. Please ensure that you have visited https://axieglobal.io to understand who we are and follow us on Discord/Twitter (@axie_global) to keep up-to-date with our latest guild offerings.

There are no public channels (as of November 2021) as the community is currently restricted to members only. We have private areas for scholars (through application) and for community builders (hiring from those who #select-a-role). Please get in touch via Twitter (@axie_global) for partnership and investment inquiries."""
    elif type == "probation_pass":
        content="""Congratulations!

We are pleased to inform you that you have passed probation. You are now officially accepted as an AxieGlobal Scholar.
A reminder that the average SLP requirement will now increase to 110 / day.

As a final request, we ask that you fill out our feedback form below. The scholar experience and wellbeing is of utmost importance to us, as we seek to continuously improve the AxieGlobal Scholarship program.
Once you have completed the feedback form, your SLP payout will occur over the next few days as they become claimable. We will confirm with you once this is complete.

We wish you all the best and look forward to further partnering with you in our Axie journey together!

https://docs.google.com/forms/d/e/1FAIpQLSfFvfMYVG79aOXYHvDsQO-5JOyQzsP1Dl8wiUhaX75CyhESdA/viewform"""
    elif type == "assign-squad":
        content="""Based on your current performance in your scholarship, you are tracking below target.
As a reminder, we have a requirement of an average 90 SLP during probation, and 110 SLP post-probation. Based on your current trajectory, you are at risk.
We have assigned a coach to you to help assist your battles in Arena. Please take this opportunity to check your squad channel, consult the coach and review your strategy."""

    elif type == "onboard":
        content="""Congratulations and welcome to AxieGlobal!
Please check your email - you account has been created and your account details and Axies have been sent to you.
You may begin your journey any time! Please raise a support ticket if you are missing Axies or have any other questions"""

    elif type == "approve":
        content="""Congratulations and welcome to AxieGlobal!
You have been accepted into an AxieGlobal Scholarship! Please see the #waitlist channel and the Scholar Terms and Conditions here: https://drive.google.com/file/d/1STnNyGHACjOK56LUGXcNCtV0zw0r1gUw/view?usp=sharing
Please begin to explore the Discord channels and get to know your guild!"""

    elif type == "terminate":
        content="""After reviewing your account, we have decided to terminate your scholarship due to not meeting the requirements.
If you were not in violation of any terms/conditions, we will have claimed and paid you your SLP.
We wish you all the best and thank you for being a part of AxieGlobal."""

    elif type == "notice":
        content="""Congratulations and welcome to AxieGlobal!
Please check your email, we have sent you an invitation link to schedule an interview. Sometimes this email end's up in the SPAM folder, be sure to double check
Our addresses are axieglobalmanager@gmail.com and axieglobal.danielurn@gmail.com .
We look foward into speak with you, please prepare yourself, study and good luck!. ♫"""

    elif type == "alert":
        content="""
        XGlobal would like to inform you that you are one of our underperforming scholars, which means you are in danger of being terminated.
In order to avoid that we would like to extend our Coaching offer to you, which is entirely free and gives you high chances of not only staying in XGlobal but improving in Axie Infinity as well! 
DM ToiletBot#8402 in order to be assigned to one of our highly-skilled coaches.
        """
    
    elif type == "warning":
        content="""
        This is XGlobal's last warning to you about your performance. 
        If you are unable to reach the quota(30slp per day average) before payment, your scholarship will be terminated. 
        If you would like to plead your case, talk to our manager Danielurn#8390. 
        """

    elif type == "added":
        content="""
            La siguiente cedula fue añadida
        """
    elif type == "duplicated":
        content="""
            La siguiente cedula presento un problema
        """

    elif type == "registerhelp":
        content="""
            Please make sure you are inserting the command as follows (without the parenthesis and just 1 space):
            
            !register (address)
            
            It must be a valid Ethereum Mainnet Address
            If you made a mistake, don't worry, just type the command again with the new address and it will be updated
        """

    elif content == "":
        content = "No embed content found"
        
    return content
