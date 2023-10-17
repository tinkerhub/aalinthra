import frappe
from frappe import get_doc

def on_lead_role(self, method):
    pass
    old_doc = self.get_doc_before_save()
    if old_doc:
            if old_doc.roles != self.roles:
                # print(f'\n\n\n old : {old_roles} \n\n\n')
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
                    permission = get_doc({
                        'doctype': 'User Permission',
                        'user': self.name, 
                        'allow': 'Learner', 
                        'for_value': self.name
                    })
                permission.save(ignore_permissions=True)
                frappe.db.commit()
                
                    
                

