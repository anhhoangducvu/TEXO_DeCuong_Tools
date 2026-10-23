import sys, glob, os, json
sys.path.insert(0,'/home/claude/proj')
from core import checker as ck
SRC="/mnt/user-data/uploads/De cuong"
sets={
 "TT02 VNM (PDF)":[f"{SRC}/TT02 261020 De-cuong-TVGS-VNM-TEXO.pdf"],
 "TT03 The Charm":sorted(glob.glob(f"{SRC}/TT03*/*.docx")),
 "TT08 Khoan KS":[glob.glob(f"{SRC}/TT08*.docx")[0]],
 "TT09 Sun Hà Nam":[f"{SRC}/TT09 250219 De cuong TVGS Sun Group Ha Nam.docx"],
 "TT09 Trắc đạc":[f"{SRC}/TT09 De cuong giam sat Trac dac.docx"],
 "TT09 Harmonia":[glob.glob(f"{SRC}/TT09 De-cuong-TVGS_Harmonia*.docx")[0]],
 "TT12 Taseco":sorted(glob.glob(f"{SRC}/TT12 250415*/*.docx")),
 "TT12 Mẫu cơ bản":[glob.glob(f"{SRC}/TT12 Mau*/*.docx")[0]],
}
out={}
for k,fs in sets.items():
    r=ck.check_files([(os.path.basename(f),f) for f in fs])
    out[k]=r
    print(f"{k:18s} mẫu={r['muc_mau']:8s} điểm={r['diem']:3d} +{r['diem_cong']} ngày={r['ngay']} từ={r['chat_luong']['so_tu']} hình={r['chat_luong']['so_hinh']} hết HL={[h['ten'] for h in r['phap_ly']['het']][:4]} mới={sum(r['phap_ly']['co_moi'].values())} trống={r['chat_luong']['so_cho_trong']} lẫn={r['chat_luong']['nghi_lan_ten'][:2]}  => {r['ket_luan']}")
json.dump(out,open('/home/claude/work/matrix.json','w'),ensure_ascii=False,indent=1,default=str)
ids=[c['id'] for c in out['TT12 Mẫu cơ bản']['tieu_chi']]
print("\nID    "+" ".join(f"{k[:6]:>6s}" for k in sets))
sym={"Đạt":"✓","Thiếu":"✗"}
for i,cid in enumerate(ids):
    row=[]
    for k in sets:
        st=out[k]['tieu_chi'][i]['trang_thai']; row.append(f"{sym.get(st,'~'):>6s}")
    print(f"{cid} {out['TT12 Mẫu cơ bản']['tieu_chi'][i]['cap']} "+" ".join(row)+"  "+out['TT12 Mẫu cơ bản']['tieu_chi'][i]['ten'][:55])
