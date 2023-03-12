odoo.define('bash_payment_report.tree_view_button', function (require){
    "use strict";
    $(document).ready(function() {
        setTimeout(_=> {
            var ListController = require('web.ListController');

            ListController.include({
                renderButtons: function($node) {
                    this._super.apply(this, arguments);
                    var self = this;

                    setTimeout(_=> {
                        let btnCondition = document.querySelectorAll('#btn-cond');
                        if (btnCondition.length !== 0) {
                            let btnAction = document.querySelectorAll('aside.o_cp_sidebar div.btn-group.o_dropdown');
                            let printBtn = btnAction[0].querySelectorAll("a[role='menuitem'].dropdown-item");
                            printBtn[0].addEventListener('click', () => {
                                var idsGet = self.getSelectedIds();
                                savedBoxSelected(idsGet);
                                for (let i=0; i<printBtn.length; i++) {
                                    setTimeout(_=> {
                                        if (i !== 0) printBtn[i].click();
                                         console.log(idsGet);
                                    }, 1000);
                                }
                            });
                        }
                    }, 3000);
                },
            });

            // CONDITION DE RESTRICTION DES MODIFICATION A UNE SEULE PAGE
            setInterval(_=> {
                onlyThisPage().then(
                    _=> {
                        printAndActionBtn()
                            .then(
                                btnAction => {
                                    $(btnAction[1]).hide();
                                    return btnAction[0].querySelectorAll("a[role='menuitem'].dropdown-item");
                                }
                            )
                            .then(
                                printBtn => {
                                    printBtn[0].innerHTML = 'Bilan Bash Payment';
                                    for (let i=1; i<printBtn.length; i++) {
                                        printBtn[i].hidden = true;
                                    }
                                }
                            )
                            .catch(error => console.log(error));
                    },
                    (error) => console.log(error)
                );

            }, 1000);

        }, 1500);

        // PROMISE
        function onlyThisPage() {
            return new Promise((resolve, reject) => {
                let btnCondition = document.querySelectorAll('#btn-cond');
                if (btnCondition.length !== 0) resolve(btnCondition);
                else reject(new Error('HTMLElement not available from ' + onlyThisPage.name + ' function'));
            });
        }
        function printAndActionBtn() {
            return new Promise((resolve, reject) => {
                let btnCondition = document.querySelectorAll('#btn-cond');
                if (btnCondition.length !== 0) {
                    let btnAction = document.querySelectorAll('aside.o_cp_sidebar div.btn-group.o_dropdown');
                    if (btnAction.length !== 0) resolve(btnAction);
                    else reject(new Error('HTMLElement not available from ' + printAndActionBtn.name + ' function'));
                }
            });
        }
        function checkTableAvailable() {
            return new Promise((resolve, reject) => {
                let btnCondition = document.querySelectorAll('#btn-cond');
                if (btnCondition.length !== 0) {
                    let ths = document.querySelectorAll('thead th');
                    let trs = document.querySelectorAll('tbody tr');
                    if (ths.length !== 0 && trs.length !==0) resolve({headCells: ths, bodyLines: trs});
                    else reject(new Error('HTMLElement not available from ' + checkTableAvailable.name + ' function'));
                }
            });
        }
        function savedBoxSelected(idsGet) {
            checkTableAvailable()
                .then(
                    table => {
                        let trs = table.bodyLines;
                        let btnCondition = document.querySelectorAll('#btn-cond');
                        if (btnCondition.length !== 0) {
                            if (idsGet.length !== 0) {
                                let rpc = require('web.rpc');
                                rpc.query({
                                    model: 'global.account.bash.payment',
                                    method: 'get_active_ids',
                                    args: [idsGet],
                                }).then(
                                    _=> console.log('Boxes checked are saved successfully in database!'),
                                    _=> console.log('Error boxes checked are not saved!!!')
                                );
                            }
                        }
                    },
                    error => console.log(error)
                )
        }

    });
});