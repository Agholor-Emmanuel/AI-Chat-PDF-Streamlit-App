css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

.chat-message {
    display: flex;
    margin-bottom: 20px;
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 10px;
}

.chat-message .avatar img {
  max-width: 40px;
  max-height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.message-container {
    max-width: 90%;
    padding: 10px;
    border-radius: 10px;
}

.user .message-container {
    background-color: #2b313e;
    align-self: flex-end;
    color: #fff;
}

.bot .message-container {
    background-color: #475063;
    align-self: flex-start;
    color: #fff;
}
</style>

'''


bot_template = '''
<div class="chat-container">
    <div class="chat-message bot">
        <div class="avatar">
            <img src="https://i.ibb.co/rM42Y8B/bot.png">
        </div>
        <div class="message-container">{{MSG}}</div>
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/8P55yRm/human.jpg">
    </div>
    <div class="message-container">{{MSG}}</div>
</div>
'''


