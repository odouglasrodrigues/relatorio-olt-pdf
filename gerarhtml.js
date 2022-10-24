const fs = require('fs');


const data = {
    content: '<!DOCTYPE html>\r\n' +
      '<html>\r\n' +
      '<!--\r\n' +
      '    WARNING! Make sure that you match all Quasar related\r\n' +
      `    tags to the same version! (Below it's "@2.10.0")\r\n` +
      '  -->\r\n' +
      '\r\n' +
      '<head>\r\n' +
      '    <link href="https://fonts.googleapis.com/css?family=Material+Icons" rel="stylesheet" type="text/css">\r\n' +
      '    <link href="https://use.fontawesome.com/releases/v5.15.4/css/all.css" rel="stylesheet" type="text/css">\r\n' +
      '    <link href="https://use.fontawesome.com/releases/v6.1.1/css/all.css" rel="stylesheet" type="text/css">\r\n' +
      '    <link href="https://cdn.jsdelivr.net/npm/quasar@2.10.0/dist/quasar.prod.css" rel="stylesheet" type="text/css">\r\n' +
      '</head>\r\n' +
      '\r\n' +
      '<body>\r\n' +
      '    <!-- example of injection point where you write your app template -->\r\n' +
      '    <div id="q-app">\r\n' +
      '\r\n' +
      '        <q-layout view="hhh lpR fFf">\r\n' +
      '\r\n' +
      '            <q-header elevated class="text-white cabecalho">\r\n' +
      '                <q-toolbar class="glossy ">\r\n' +
      '                    <q-toolbar-title>\r\n' +
      '                        <div class="fit row  justify-between items-center content-center">\r\n' +
      '                            <div class="logoToolbar"><img src="Logo TP.png" style="width: 180px;"></div>\r\n' +
      '                            <div class="titleToolbar">Relatório de Rede</div>\r\n' +
      '                            <div class="infoToolbar justify-center items-center content-center"> Relatório gerado em:\r\n' +
      '                                <div>{{data}} - {{hora}}</div>\r\n' +
      '                            </div>\r\n' +
      '                        </div>\r\n' +
      '\r\n' +
      '\r\n' +
      '\r\n' +
      '                    </q-toolbar-title>\r\n' +
      '                </q-toolbar>\r\n' +
      '            </q-header>\r\n' +
      '\r\n' +
      '            <q-page-container>\r\n' +
      '                <h1>Teste</h1>\r\n' +
      '                {{jsonData}}\r\n' +
      '            </q-page-container>\r\n' +
      '\r\n' +
      '        </q-layout>\r\n' +
      '\r\n' +
      '    </div>\r\n' +
      '\r\n' +
      '    <!-- Add the following at the end of your body tag -->\r\n' +
      '    <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.prod.js"></script>\r\n' +
      '    <script src="https://cdn.jsdelivr.net/npm/quasar@2.10.0/dist/quasar.umd.prod.js"></script>\r\n' +
      '    <script src="https://cdn.jsdelivr.net/npm/quasar@2.10.0/dist/lang/pt-BR.umd.prod.js"></script>\r\n' +
      '\r\n' +
      '    <script>\r\n' +
      '        const { useQuasar } = Quasar\r\n' +
      '\r\n' +
      '\r\n' +
      '        const app = Vue.createApp({\r\n' +
      '            setup() {\r\n' +
      '                const $q = useQuasar()\r\n' +
      '\r\n' +
      '                return {\r\n' +
      '                    data: "24/10/2022",\r\n' +
      '                    hora: "14:09"\r\n' +
      '                }\r\n' +
      '            },\r\n' +
      '            data() {\r\n' +
      '                return { jsonData: {}, novoJson: {} }\r\n' +
      '\r\n' +
      '            },\r\n' +
      '            methods: {\r\n' +
      '                async GetJson() {\r\n' +
      "                    fetch('./dados.json', {\r\n" +
      "                        method: 'GET',\r\n" +
      "                        mode: 'cors',\r\n" +
      "                        cache: 'default'\r\n" +
      '                    })\r\n' +
      '                        .then(res => res.json())\r\n' +
      '                        .then(data => {\r\n' +
      '                            this.jsonData = data\r\n' +
      '                        })\r\n' +
      '\r\n' +
      '                }\r\n' +
      '            },\r\n' +
      '            created() {\r\n' +
      '                this.GetJson()\r\n' +
      "                $.getJSON('./dados.json',).then(data => {\r\n" +
      '                    this.novoJson = data\r\n' +
      '                })\r\n' +
      '\r\n' +
      '            },\r\n' +
      '        })\r\n' +
      '\r\n' +
      '        app.use(Quasar, { config: {} })\r\n' +
      "        app.mount('#q-app')\r\n" +
      '    </script>\r\n' +
      '\r\n' +
      '    <style>\r\n' +
      "        @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,500&display=swap');\r\n" +
      '\r\n' +
      '        body,\r\n' +
      '        html {\r\n' +
      "            font-family: 'Poppins', sans-serif;\r\n" +
      '        }\r\n' +
      '\r\n' +
      '        .cabecalho {\r\n' +
      '            background: rgb(13, 36, 102);\r\n' +
      '        }\r\n' +
      '\r\n' +
      '        .titleToolbar {\r\n' +
      '            font-size: 35px;\r\n' +
      '            margin-left: -40px;\r\n' +
      '        }\r\n' +
      '\r\n' +
      '        .infoToolbar {\r\n' +
      '            font-size: 10px;\r\n' +
      '        }\r\n' +
      '    </style>\r\n' +
      '</body>\r\n' +
      '\r\n' +
      '</html>'
  }


//const fileInHtml = { content: fs.readFileSync('data.html', 'utf8') };

fs.writeFileSync('teste.html', data.content, 'utf8' )

//console.log(fileInHtml)