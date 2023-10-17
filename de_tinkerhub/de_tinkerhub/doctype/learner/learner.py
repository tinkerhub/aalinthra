# Copyright (c) 2023, D-codE and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Learner(WebsiteGenerator):

	def autoname(self):
		# select a project name based on customer
		self.name = self.user	

	def get_context(self, context):

		user_roles = frappe.get_roles()
		if 'Event Admin' in user_roles:
			context.event_admin = True
		else:
			context.event_admin = False

		context.show_sidebar = 1
		if self.college:
			context.college_name = frappe.db.get_value('College', self.college, 'college_name') 

	def validate(self):
		if not self.route:
			self.route = f"learner/{self.name}"

		if self.user != self.email:
			if self.user:
				self.email = self.user
			elif self.email:
				self.user = self.email

	def on_update(self):
		restrict_profile = '1'	
		if self.college_student and self.mobile_no and self.full_name:
			restrict_profile = '0'
			
		frappe.db.set_value('Learner', self.name, 'restrict_profile', restrict_profile)
		frappe.db.commit()

# 		old_doc = self.get_doc_before_save()




	
	


	


