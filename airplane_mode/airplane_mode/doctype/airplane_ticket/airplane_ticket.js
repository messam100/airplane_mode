// Copyright (c) 2025, Mohammed Al-Qershi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(
                "Assign Seat",
                function () {
                    let dialog = new frappe.ui.Dialog({
                        title: "Select Seat",
                        fields: [
                            {
                                label: "Seat Number",
                                fieldname: "seat_number",
                                fieldtype: "Data",
                                // options: "Airplane Seat",
                                reqd: 1,
                                // get_query: function () {
                                //     return {
                                //         filters: {
                                //             airplane_flight: frm.doc.flight,
                                //             status: "Available"
                                //         }
                                //     };
                                // }
                            },
                        ],
                        primary_action_label: "Assign",
                        primary_action(values) {
                            frm.set_value("seat", values.seat_number);
                            dialog.hide();
                            frm.save();
                        },
                    });

                    dialog.show();
                },
                __("Actions")
            );
        }
    },
});
