#!/bin/bash
# Fill ALL Vantiv eProtect iframe fields in a single CDP WebSocket call
# Usage: fill-vantiv-all.sh <card_number> <exp_month_2digit> <exp_year_2digit> <cvv> [port]
# Example: fill-vantiv-all.sh 4147099111428502 11 26 619

CARD="$1"
MONTH="$2"
YEAR="$3"
CVV="$4"
PORT="${5:-18800}"

if [ -z "$CARD" ] || [ -z "$MONTH" ] || [ -z "$YEAR" ] || [ -z "$CVV" ]; then
  echo "Usage: fill-vantiv-all.sh <card_number> <exp_month> <exp_year> <cvv> [port]"
  exit 1
fi

# Find Vantiv iframe WebSocket URL
WS_URL=$(curl -s "http://127.0.0.1:${PORT}/json" | python3 -c "
import sys, json
for t in json.load(sys.stdin):
    if 'eprotect' in t.get('url',''):
        print(t['webSocketDebuggerUrl']); break
" 2>/dev/null)

if [ -z "$WS_URL" ]; then
  echo "ERROR: Vantiv iframe not found. Make sure you're on the DSW pay step."
  exit 1
fi

# Set ALL fields in one CDP call: card number, expiry month, expiry year, CVV
node --experimental-websocket -e "
const ws = new WebSocket('${WS_URL}');
ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: \"(function(){var setter=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;var cn=document.getElementById('accountNumber');var mo=document.getElementById('expMonth');var yr=document.getElementById('expYear');var cv=document.getElementById('cvv');setter.call(cn,'${CARD}');cn.dispatchEvent(new Event('input',{bubbles:true}));cn.dispatchEvent(new Event('change',{bubbles:true}));mo.value='${MONTH}';mo.dispatchEvent(new Event('change',{bubbles:true}));yr.value='${YEAR}';yr.dispatchEvent(new Event('change',{bubbles:true}));setter.call(cv,'${CVV}');cv.dispatchEvent(new Event('input',{bubbles:true}));cv.dispatchEvent(new Event('change',{bubbles:true}));return 'card=...'+cn.value.slice(-4)+' month='+mo.value+' year='+yr.value+' cvv_len='+cv.value.length})()\"
    }
  }));
};
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  if(msg.id===1){console.log(msg.result.value||JSON.stringify(msg.result));ws.close();process.exit(0);}
};
ws.onerror = () => {console.error('WebSocket error');process.exit(1);};
setTimeout(()=>{console.error('Timeout');process.exit(1);},5000);
" 2>&1
