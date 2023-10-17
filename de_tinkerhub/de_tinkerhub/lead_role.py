import frappe
from frappe import get_doc

def on_lead_role(self, method):
    user_id = self.email
    f_name = self.full_name
    first_name = self.first_name

    if not frappe.db.exists({"doctype":"Learner","email": user_id}):
        learner = get_doc({
            "doctype": "Learner",
            "user": user_id,
            "email": user_id,
            "is_published": 1
        })
        learner.save(ignore_permissions=True)
        frappe.db.commit()
        user_doc = get_doc('User', user_id)
        # assign learner role      
        user_doc.append('roles', {
            'role': 'Learner'
        })
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        permission = get_doc({
            "doctype": "User Permission",
            "user": user_id,
            "allow": 'Learner',
            "for_value": self.email
        })
        permission.save(ignore_permissions=True)
        
        frappe.db.commit()

    else:
        old_doc = self.get_doc_before_save()
        if old_doc.roles != self.roles :
            roles = frappe.get_all(
                'Has Role',
                filters={'parent': self.name},
                fields=['role']
            )
            cur_roles = [item['role'] for item in roles]
            college = frappe.db.get_value('Learner', self.name, 'college')
            if 'Campus Lead' in cur_roles and not frappe.db.exists('User Permission', {'user': self.name, 'allow': 'College', 'for_value': college}):
                if college:
                    permission = get_doc({
                        'doctype': 'User Permission',
                        'user': self.name, 
                        'allow': 'College', 
                        'for_value': college
                    })
                    frappe.db.delete("User Permission", {
                        'user': self.name, 
                        'allow': 'Learner', 
                        'for_value': self.name
                    })
                    
            else:
                frappe.db.delete("User Permission", {
                    'user': self.name, 
                    'allow': 'College', 
                    'for_value': college
                })
                if not frappe.db.exists({"doctype":"User Permission","user": user_id, "allow": 'Learner', "for_value": self.email}):
                    permission = get_doc({
                        'doctype': 'User Permission',
                        'user': self.name, 
                        'allow': 'Learner', 
                        'for_value': self.name
                    })
                    
            # frappe.db.commit()
            try:
                permission.save(ignore_permissions=True)
                frappe.db.commit()
            except frappe.exceptions.LinkValidationError as e:
                # Log the error and print a message for debugging
                frappe.logger().error(f"LinkValidationError: {str(e)}")
                    

                    
            

