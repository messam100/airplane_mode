// Copyright (c) 2025, Mohammed Al-Qershi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rent Payment", {
    onload(frm) {
        if (frm.is_new()) {
            frappe.db.get_single_value("Shop Settings", "default_rent").then(value => {
                if (value) {
                    frm.set_value("amount_paid", value);
                }
            });
        }
    }
});
