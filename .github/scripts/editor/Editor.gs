/* =====================================================================
   EDITOR DE ANÚNCIOS LumiFa — Google Apps Script da planilha CATALOGO
   Recebe os pedidos do site (modo equipe) e grava na aba Página1:
     - arquivar / desarquivar  -> coluna "status" (Ativo / Arquivado)
     - editar                  -> nome, categoria, preco, especificacoes, descricao
   Tudo que muda fica registrado na aba "Histórico_Editor" (com o valor antigo).

   COMO INSTALAR (uma vez só):
   1. Na planilha CATALOGO: Extensões > Apps Script.
   2. Apague o que estiver lá, cole este arquivo inteiro.
   3. Troque a senha abaixo pela MESMA senha do modo equipe do site.
   4. Salvar > Implantar > Nova implantação > tipo "App da Web":
        Executar como: Eu  |  Quem pode acessar: Qualquer pessoa
   5. Autorize e copie o "URL do app da Web" (termina em /exec).
   Ao mudar o código depois: Implantar > Gerenciar implantações > lápis >
   Versão: "Nova versão" (assim o link continua o mesmo).
   ===================================================================== */

const SENHA = 'COLOQUE_AQUI_A_SENHA_DA_EQUIPE';

const ABA = 'Página1';
const ABA_HIST = 'Histórico_Editor';
const EDITAVEIS = ['nome', 'categoria', 'preco', 'especificacoes', 'descricao'];

function doGet() {
  return json_({ ok: true, editor: 'LumiFa', versao: 1 });
}

function doPost(e) {
  let r;
  try { r = processar_(JSON.parse(e.postData.contents)); }
  catch (err) { r = { ok: false, erro: String(err && err.message || err) }; }
  return json_(r);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function processar_(req) {
  if (!req || String(req.senha || '') !== SENHA) return { ok: false, erro: 'Senha incorreta' };
  if (req.acao === 'ping') return { ok: true };
  if (['arquivar', 'desarquivar', 'editar'].indexOf(req.acao) < 0) return { ok: false, erro: 'Ação desconhecida' };

  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(ABA);
    const lastCol = sh.getLastColumn();
    const head = sh.getRange(1, 1, 1, lastCol).getValues()[0].map(h => String(h).trim().toLowerCase());
    let cStatus = head.indexOf('status') + 1;
    if (!cStatus) { cStatus = lastCol + 1; sh.getRange(1, cStatus).setValue('status'); head.push('status'); }

    const n = sh.getLastRow() - 1;
    const codes = sh.getRange(2, 1, n, 1).getValues().map(r => String(r[0]).trim().toUpperCase());
    const lista = (req.codigos || []).map(c => String(c).trim().toUpperCase()).filter(Boolean);
    if (!lista.length) return { ok: false, erro: 'Nenhum código informado' };

    const agora = new Date();
    const hist = [];
    const feitos = [], faltando = [];

    lista.forEach(code => {
      const i = codes.indexOf(code);
      if (i < 0) { faltando.push(code); return; }
      const row = i + 2;

      if (req.acao === 'arquivar' || req.acao === 'desarquivar') {
        const novo = req.acao === 'arquivar' ? 'Arquivado' : 'Ativo';
        const cell = sh.getRange(row, cStatus);
        const antes = String(cell.getValue() || 'Ativo');
        if (antes !== novo) { cell.setValue(novo); hist.push([agora, req.acao, code, 'status', antes, novo]); }
      } else {
        const dados = req.dados || {};
        EDITAVEIS.forEach(campo => {
          if (!(campo in dados)) return;
          const c = head.indexOf(campo) + 1;
          if (!c) return;
          const cell = sh.getRange(row, c);
          const antes = String(cell.getDisplayValue());
          const depois = String(dados[campo] == null ? '' : dados[campo]).trim();
          if (antes === depois) return;
          if (campo === 'preco') cell.setNumberFormat('@');   // preço fica como texto "81,18", igual ao resto
          cell.setValue(depois);
          hist.push([agora, 'editar', code, campo, antes, depois]);
        });
      }
      feitos.push(code);
    });

    if (hist.length) {
      let h = ss.getSheetByName(ABA_HIST);
      if (!h) { h = ss.insertSheet(ABA_HIST); h.appendRow(['data', 'acao', 'codigo', 'campo', 'antes', 'depois']); }
      h.getRange(h.getLastRow() + 1, 1, hist.length, 6).setValues(hist);
    }
    SpreadsheetApp.flush();
    return { ok: true, feitos: feitos, faltando: faltando, mudancas: hist.length };
  } finally {
    lock.releaseLock();
  }
}
