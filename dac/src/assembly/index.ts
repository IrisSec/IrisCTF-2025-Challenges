let wasmSecretData: Uint8Array = new Uint8Array(0);
let wasmDataView: DataView = new DataView(wasmSecretData.buffer);
let secretPhase: i32 = -1;
let secretStr: string = "";

// getSecretStr
export function reality(): string {
  return secretStr;
}

// getSecretPhase
export function perception(): i32 {
  return secretPhase;
}

// setSecretData
export function recognition(jsSecretData: Uint8Array): void {
  wasmSecretData = new Uint8Array(jsSecretData.byteLength);
  wasmSecretData.set(jsSecretData);
  wasmDataView = new DataView(wasmSecretData.buffer);
  secretPhase = 0;
}

// getPixel
function _d1d74bf4a5d31cd8919be44ea3215a15(x: u32, y: u32, w: u32, h: u32, doff: u32): u32 {
  const pixelOff: i32 = doff + (h - 1 - y) * w * 4 + x * 4;
  return wasmDataView.getUint32(pixelOff, true);
}

// setPixel
function _cea50859a4b4ea0648efa7cfd971e108(x: u32, y: u32, v: u32, w: u32, h: u32, doff: u32): void {
  const pixelOff: i32 = doff + (h - 1 - y) * w * 4 + x * 4;
  wasmDataView.setUint32(pixelOff, v, true);
}

// getNextChalInfo
export function consciousness(catIdx: u32): string {
  const c: string = "?";
  if (wasmSecretData.byteLength === 0 || wasmDataView.byteLength === 0) {
    return "";
  }
  
  if (secretPhase === 0 && catIdx !== 3) {
    return "";
  } else if (secretPhase === 1 && catIdx !== 5) {
    return "";
  } else if (secretPhase === 2 && catIdx !== 6) {
    return "";
  } else if (secretPhase === 3 && catIdx !== 1) {
    return "";
  } else if (secretPhase === 4 && catIdx !== 8) {
    return "";
  } else if (secretPhase > 4) {
    return "";
  }

  return `{"id":${999999999},"title":"${c.repeat(16)}","description":"${c.repeat((((secretPhase+1)*101)%40)+15)} ${c.repeat((((secretPhase+1)*202)%40)+15)} ${c.repeat((((secretPhase+1)*303)%40)+15)} ${c.repeat((((secretPhase+1)*404)%40)+15)} ${c.repeat((((secretPhase+1)*505)%40)+15)} ${c.repeat((((secretPhase+1)*606)%40)+15)} ${c.repeat((((secretPhase+1)*707)%40)+15)}","authors":"us","points":500,"exposed":1,"relies_on":0,"flaggable":1,"tags":"impossible","targets":[],"files":[],"hints":[],"solves":0,"solve_position":0,"last_submission":0}`;
}

// loFlipSingle
function _1f0b54b0da3936d69a48c380b350562d(sx: u32, sy: u32, x: u32, y: u32, w: u32, h: u32, doff: u32): void {
  _cea50859a4b4ea0648efa7cfd971e108(sx + x, sy + y, _d1d74bf4a5d31cd8919be44ea3215a15(sx + x, sy + y, w, h, doff) ^ 0x100, w, h, doff);
}

// loTap
function _e31ca4c06fe401d361404281fac5b217(sx: u32, sy: u32, x: u32, y: u32, w: u32, h: u32, doff: u32): void {
  _1f0b54b0da3936d69a48c380b350562d(sx, sy, x, y, w, h, doff);
  if (x != 0) {
    _1f0b54b0da3936d69a48c380b350562d(sx, sy, x - 1, y, w, h, doff);
  }
  if (x != 5) {
    _1f0b54b0da3936d69a48c380b350562d(sx, sy, x + 1, y, w, h, doff);
  }
  if (y != 0) {
    _1f0b54b0da3936d69a48c380b350562d(sx, sy, x, y - 1, w, h, doff);
  }
  if (y != 5) {
    _1f0b54b0da3936d69a48c380b350562d(sx, sy, x, y + 1, w, h, doff);
  }
}

// inverseCantor
function _712551dd45fb0e445d9535da25eb4344(z: u32): u32 {
  const w: u32 = u32(Math.floor((Math.sqrt(8 * z + 1) - 1) / 2));
  const t: u32 = (w * (w + 1)) / 2;
  const y: u32 = z - t;
  const x: u32 = w - y;
  return x | (y << 8);
}

function doAwareness(str: string, rectX: u32, rectY: u32, width: u32, height: u32, dataOffset: u32): boolean {
  const alpha: string = "abcdefghijklmnopqrstuvwxyz0123456789";
  for (let i: i32 = 0; i < 12; i++) {
    const alphaCharIdx = alpha.indexOf(str.charAt(i));
    if (alphaCharIdx === -1) {
      return false;
    }

    const boardParts: u32 = _712551dd45fb0e445d9535da25eb4344(alphaCharIdx);
    const board0Part: u32 = boardParts & 0xff;
    const board1Part: u32 = (boardParts >> 8) & 0xff;
    const side: u32 = i % 2;
    const row: u32 = i / 2;
    if (board0Part & 1) {
      _e31ca4c06fe401d361404281fac5b217(rectX, rectY, side * 3 + 0, row, width, height, dataOffset);
    }
    if (board0Part & 2) {
      _e31ca4c06fe401d361404281fac5b217(rectX, rectY, side * 3 + 1, row, width, height, dataOffset);
    }
    if (board0Part & 4) {
      _e31ca4c06fe401d361404281fac5b217(rectX, rectY, side * 3 + 2, row, width, height, dataOffset);
    }
    if (board1Part & 1) {
      _e31ca4c06fe401d361404281fac5b217(rectX + 6, rectY, side * 3 + 0, row, width, height, dataOffset);
    }
    if (board1Part & 2) {
      _e31ca4c06fe401d361404281fac5b217(rectX + 6, rectY, side * 3 + 1, row, width, height, dataOffset);
    }
    if (board1Part & 4) {
      _e31ca4c06fe401d361404281fac5b217(rectX + 6, rectY, side * 3 + 2, row, width, height, dataOffset);
    }
  }

  return true;
}

// checkSecret
export function awareness(str: string): bool {
  const dataOffset: u32 = wasmDataView.getUint32(0xa, true);
  const width: u32 = wasmDataView.getUint32(0x12, true);
  const height: u32 = wasmDataView.getUint32(0x16, true);

  const rectPosEnc: u32 = _d1d74bf4a5d31cd8919be44ea3215a15(0, secretPhase, width, height, dataOffset);
  const rectX: u32 = (rectPosEnc >> 8) & 0xff;
  const rectY: u32 = (rectPosEnc     ) & 0xff;

  if (str.length !== 12) {
    return false;
  }

  let success: boolean = doAwareness(str, rectX, rectY, width, height, dataOffset);
  for (let chkY: u32 = 0; chkY < 6; chkY++) {
    for (let chkX: u32 = 0; chkX < 6; chkX++) {
      const p0: u32 = _d1d74bf4a5d31cd8919be44ea3215a15(rectX + chkX, rectY + chkY, width, height, dataOffset);
      const p1: u32 = _d1d74bf4a5d31cd8919be44ea3215a15(rectX + 6 + chkX, rectY + chkY, width, height, dataOffset);
      if ((p0 & 0x100) > 0 || (p1 & 0x100) > 0) {
        success = false;
      }
    }
  }

  if (!success) {
    doAwareness(str, rectX, rectY, width, height, dataOffset);
    return false;
  }

  secretPhase++;
  secretStr += str;
  return true;
}