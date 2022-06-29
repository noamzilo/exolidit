import dtlpy as dl

# email, password = r"noam.s@uveye.com", r"Hamburg%20"
# email, password = r"sapir.a@uveye.com", r"Sa!204187470"
# dtlpy.login_m2m(email=email, password=password)

dl.login()
project = dl.projects.get(project_name='noam_test')
bot_creds = project.bots.create(name='noam_bot', return_credentials=True)

bot_mail = bot_creds.email
bot_pass = bot_creds.password

print(f"mail: {bot_mail}, password: {bot_pass}")

# email, password = r"noam.s@uveye.com", r"Hamburg%20"
# email, password = r"sapir.a@uveye.com", r"Sa!204187470"