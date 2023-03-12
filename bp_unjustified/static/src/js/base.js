odoo.define('bp_unjustified.Base', function (require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;

    var AbstractService = require('web.AbstractService');
    var Notification = require('web.Notification');
    var core = require('web.core');
    var Notification = require('web.Notification');

    $(document).ready(function() {

        let mutationObject = { target: document.body };

        var observer = new MutationObserver(function(mutations) {
            if (document.contains($('div.o_notification_manager')[0])) {
                const bodyWidth = $('body').css('width');
                let targetNode = document.querySelector('div.o_notification_manager');

                let notifications = targetNode.querySelectorAll('div.o_notification');
                const condition = notifications[0].querySelector('.o_notification_content');
                if ($(condition).text().substring(0, 14) === 'bp_unjustified') {
                    targetNode.style.width = bodyWidth;
                    for (let notification of notifications) {
                        let title = notification.querySelector('.o_notification_title');
                        let content = notification.querySelector('.o_notification_content');
                        $(title).text('Vos bons provisoires non justifiés');
                        title.style.width = bodyWidth;
                        $(title).css('text-transform', 'uppercase');
                        $(title).css('text-align', 'center');

                        const contentHtml = $(content).html();
                        let tableLines = [];
                        tableLines = contentHtml.split('<br><br>');
                        let table = convertContentToTable(tableLines)
                        table.style.width = bodyWidth;
                        $(table).css('border-collapse', 'collapse').css('left', '0px');
                        let ths = table.querySelectorAll('th');
                        let tds = table.querySelectorAll('td');
                        for (let i=0; i<ths.length; i++)
                            $(ths[i]).css('border', '1px solid white').css('padding-left', '0.4rem');

                        for (let i=0; i<tds.length; i++) {
                            $(tds[i]).css('border', '1px solid gray').css('padding-left', '0.4rem');
                            if (! isNaN(parseInt($(tds[i]).text().replace(/ +/g, ''))))
                                $(tds[i]).css('text-align', 'right').css('padding-right', '1rem');
                        }

                        $(content).html(table);
                    }
                }
                observer.disconnect();
            }
        });

        observer.observe(mutationObject.target, {attributes: false, childList: true, characterData: true, subtree:true});

        setInterval(_=> {
            getNotifications()
                .then(
                    notification => {
                        let title = notification.querySelector('.o_notification_title');
                        let content = notification.querySelector('.o_notification_content');
                        if ($(content).text().substring(0, 14) === 'bp_unjustified') {
                            if (content.firstElementChild.nodeName.toLocaleLowerCase() !== 'table') {
                                const bodyWidth = $('body').css('width');
                                $(title).text('Vos bons provisoires non justifiés');
                                title.style.width = bodyWidth;
                                $(title).css('text-transform', 'uppercase');
                                $(title).css('text-align', 'center');

                                const contentHtml = $(content).html();
                                let tableLines = [];
                                tableLines = contentHtml.split('<br><br>');
                                let table = convertContentToTable(tableLines)
                                table.style.width = bodyWidth;
                                $(table).css('border-collapse', 'collapse').css('left', '0px');
                                let ths = table.querySelectorAll('th');
                                let tds = table.querySelectorAll('td');
                                for (let i=0; i<ths.length; i++)
                                    $(ths[i]).css('border', '1px solid white').css('padding-left', '0.4rem');

                                for (let i=0; i<tds.length; i++) {
                                    $(tds[i]).css('border', '1px solid gray').css('padding-left', '0.4rem');
                                    if (! isNaN(parseInt($(tds[i]).text().replace(/ +/g, ''))))
                                        $(tds[i]).css('text-align', 'right').css('padding-right', '1rem');
                                }

                                $(content).html(table);
                            }
                        }
                    }
                );
        }, 500);

        // FUNCTIONS
        function convertContentToTable(tableString = []) {
            // CREATING THEAD
            let thead = document.createElement('thead');
            let trh = document.createElement('tr');
            for (let i=1; i<=6; i++) {
                let th = document.createElement('th');
                if (i === 1) {
                    th.innerHTML = 'No';
                    trh.appendChild(th);
                }
                if (i === 2) {
                    th.innerHTML = 'Description';
                    trh.appendChild(th);
                }
                if (i === 3) {
                    th.innerHTML = 'Bénéficiaire';
                    trh.appendChild(th);
                }
                if (i === 4) {
                    th.innerHTML = 'Initiateur';
                    trh.appendChild(th);
                }
                if (i === 5) {
                    th.innerHTML = 'Date';
                    trh.appendChild(th);
                }
                if (i === 6) {
                    th.innerHTML = 'Montant';
                    trh.appendChild(th);
                }
            }
            thead.appendChild(trh);

            // CREATING TBODY
            let tbody = document.createElement('tbody');
            for (const line of tableString) {
                let cells = line.split('<br>');
                let trb = document.createElement('tr');
                for (const cell of cells) {
                    let td = document.createElement('td');
                    if (cell !== '') {
                        const index = cell.indexOf(':');
                        td.innerHTML = cell.substring(index+1).trim();
                        trb.appendChild(td);
                    }
                }
                tbody.appendChild(trb);
            }

            // CHANGE CONTENT TO TABLE
            let table = document.createElement('table');
            table.appendChild(thead);
            table.appendChild(tbody);

            return table;
        }

        // PROMISES
        function getNotifications() {
            return new Promise((resolve, reject) => {
                let notifications = document.querySelectorAll('div.o_notification');
                if (notifications.length !== 0) {
                    let notification = notifications[notifications.length - 1];
                    resolve(notification);
                }
            });
        }
    });


    //ajax.loadXML('/bp_unjustified/static/src/xml/base.xml', qweb);
});