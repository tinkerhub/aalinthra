import frappe
import datetime

no_cache = 1
no_sitemap = 1

from de_tinkerhub.de_tinkerhub.utils import (
	get_restriction_details,
    add_nav
)


def get_context(context):
    events = []

    user_roles = frappe.get_roles()
    if 'Event Admin' in user_roles:
        context.event_admin = True
    else:
        context.event_admin = False

    restriction = get_restriction_details()
    context.restriction = restriction

    query = frappe.db.sql_list(f"""
    SELECT te.name
    FROM `tabTinkerHub Event` as te
    WHERE 
        starting_date >= CURDATE() AND
        status = 'Confirmed' AND
        is_published = 1 AND
        (public_event = 1 OR host_college IN (
            SELECT college FROM `tabLearner` WHERE name = '{frappe.session.user}'
        ));

    """)


    if query:
        events = frappe.db.get_list(
			'TinkerHub Event',
			filters = {
				'name': ['in', query]
			},
			fields = ['name','starting_date', 'title', 'host_college']
    	)

    context.events = events
    context.show_sidebar = 1
    context.no_cache = 1
    return context

