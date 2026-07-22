# style.py
import streamlit as st

def apply_mobile_app_style():
    st.markdown("""
<style>

@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

*{
    font-family:'Pretendard',sans-serif;
    box-sizing:border-box;
}

html,
body,
.stApp{
    background:#F6F1EC;
    color:#222;
}

/* Streamlit 제거 */

header{visibility:hidden;}
footer{visibility:hidden;}
#MainMenu{visibility:hidden;}

/* 앱 배경 */

[data-testid="stAppViewContainer"]{
    background:#F6F1EC;
}

/* 모바일 프레임 */

.main .block-container{

    max-width:430px;

    margin:auto;

    background:#FFF8F5;

    min-height:100vh;

    padding-top:70px;

    padding-left:18px;

    padding-right:18px;

    padding-bottom:90px;

    border-radius:30px;

    box-shadow:
    0 20px 45px rgba(0,0,0,.18);

    overflow:hidden;

}

/* 스크롤 */

::-webkit-scrollbar{
    width:0;
    height:0;
}

/* Header */

.sticky-header{

position:fixed;

top:0;

left:50%;

transform:translateX(-50%);

width:100%;

max-width:430px;

height:62px;

background:rgba(255,248,245,.95);

backdrop-filter:blur(18px);

display:flex;

justify-content:space-between;

align-items:center;

padding:0 22px;

z-index:9999;

border-bottom:1px solid #EFE7E2;

border-radius:30px 30px 0 0;

}

.header-left{
display:flex;
flex-direction:column;
}

.header-small{
font-size:12px;
color:#888;
font-weight:600;
}

.header-title{
font-size:22px;
font-weight:800;
color:#222;
margin-top:2px;
}

/* 카드 공통 */

.card{

background:white;

border-radius:22px;

padding:18px;

margin-bottom:18px;

box-shadow:
0 5px 18px rgba(0,0,0,.05);

border:1px solid #F3ECE8;

transition:.25s;

}

.card:hover{
transform:translateY(-2px);
}

/* 잔액 카드 */

.balance-card{

position:relative;

overflow:hidden;

background:linear-gradient(
135deg,
#FF7477,
#FF6363
);

color:white;

border:none;

box-shadow:
0 10px 30px rgba(255,98,98,.25);

}

.balance-card::after{

content:"";

position:absolute;

right:-25px;

top:-20px;

width:120px;

height:120px;

border-radius:50%;

background:rgba(255,255,255,.12);

}

.balance-title{
font-size:13px;
opacity:.9;
font-weight:600;
}

.balance-money{
font-size:30px;
font-weight:900;
margin-top:10px;
margin-bottom:20px;
letter-spacing:-1px;
}

.balance-row{
display:flex;
justify-content:space-between;
border-top:1px solid rgba(255,255,255,.15);
padding-top:14px;
}

.balance-item{
width:48%;
}

.balance-label{
font-size:12px;
opacity:.8;
}

.balance-value{
font-size:18px;
font-weight:800;
margin-top:5px;
}

/* 수입/지출 카드 */

.mini-card{
padding:16px;
border-radius:18px;
background:white;
border:1px solid #F1EBE8;
box-shadow:0 4px 12px rgba(0,0,0,.03);
}

.mini-label{
font-size:12px;
font-weight:700;
color:#888;
margin-bottom:8px;
}

.mini-income{
color:#58D5C9;
font-size:22px;
font-weight:900;
}

.mini-expense{
color:#FF7070;
font-size:22px;
font-weight:900;
}

/* 섹션 제목 */

.section-title{
display:flex;
justify-content:space-between;
align-items:center;
margin:6px 0 14px 0;
}

.section-title h3{
margin:0;
font-size:17px;
font-weight:800;
}

.section-link{
font-size:13px;
font-weight:700;
color:#FF6B6B;
}

/* 카테고리 가로 스크롤 */

.cat-grid{
display:flex;
gap:10px;
overflow-x:auto;
padding-bottom:6px;
}

.cat-box{
min-width:84px;
background:white;
border:1px solid #F1EBE8;
border-radius:18px;
padding:12px 10px;
text-align:center;
box-shadow:0 2px 8px rgba(0,0,0,.02);
}

.cat-icon{
font-size:22px;
margin-bottom:6px;
}

.cat-name{
font-size:12px;
font-weight:700;
color:#555;
}

.cat-amt{
font-size:13px;
font-weight:900;
color:#FF6B6B;
margin-top:4px;
}

/* 캘린더 */

.calendar-card{
padding:16px;
}

.calendar-header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:12px;
}

.calendar-month{
font-size:20px;
font-weight:900;
}

.calendar-nav{
display:flex;
gap:8px;
}

.calendar-nav-btn{
width:36px;
height:36px;
border-radius:50%;
background:white;
border:1px solid #EFE7E2;
display:flex;
align-items:center;
justify-content:center;
font-weight:800;
color:#666;
box-shadow:0 2px 6px rgba(0,0,0,.03);
}

.calendar-table{
width:100%;
border-collapse:separate;
border-spacing:0;
table-layout:fixed;
}

.calendar-table th{
padding:10px 0;
font-size:12px;
font-weight:800;
color:#888;
}

.calendar-table td{
height:72px;
vertical-align:top;
padding:4px;
}

.day-box{
width:100%;
height:64px;
border-radius:16px;
padding:6px 4px;
background:white;
border:1px solid transparent;
display:flex;
flex-direction:column;
align-items:center;
gap:4px;
}

.day-box:hover{
background:#FFF4F2;
}

.day-number{
font-size:14px;
font-weight:800;
color:#222;
line-height:1;
}

.day-box.selected{
background:#FFF1F1;
border-color:#FFB8B8;
}

.day-box.selected .day-number{
background:#FF6B6B;
color:white;
width:28px;
height:28px;
border-radius:50%;
display:flex;
align-items:center;
justify-content:center;
}

.sun{ color:#FF6B6B !important; }
.sat{ color:#4A8CFF !important; }

.day-pill{
padding:2px 6px;
border-radius:999px;
font-size:10px;
font-weight:800;
line-height:1;
}

.day-pill.income{
background:#E9FAF7;
color:#16B7A2;
}

.day-pill.expense{
background:#FFEDED;
color:#FF7070;
}

/* 거래 내역 */

.tx-card{
padding:16px;
display:flex;
align-items:center;
justify-content:space-between;
gap:12px;
}

.tx-left{
display:flex;
align-items:center;
gap:12px;
min-width:0;
}

.tx-icon{
width:48px;
height:48px;
border-radius:16px;
background:#FFF3EF;
display:flex;
align-items:center;
justify-content:center;
font-size:22px;
flex-shrink:0;
}

.tx-info{
min-width:0;
}

.tx-title{
font-size:15px;
font-weight:800;
color:#222;
white-space:nowrap;
overflow:hidden;
text-overflow:ellipsis;
}

.tx-sub{
font-size:12px;
color:#999;
margin-top:2px;
white-space:nowrap;
overflow:hidden;
text-overflow:ellipsis;
}

.tx-right{
text-align:right;
flex-shrink:0;
}

.tx-plus{
color:#58D5C9;
font-size:16px;
font-weight:900;
}

.tx-minus{
color:#FF7070;
font-size:16px;
font-weight:900;
}

/* 빈 상태 */

.empty-box{
text-align:center;
padding:36px 20px;
color:#AAA;
font-size:14px;
}

/* FAB */

.fab-wrap{
position:fixed;
bottom:82px;
left:50%;
transform:translateX(-50%);
width:100%;
max-width:430px;
padding:0 22px;
pointer-events:none;
z-index:9999;
}

.fab{
margin-left:auto;
width:116px;
height:50px;
border-radius:30px;
background:#FF6B6B;
color:white;
display:flex;
align-items:center;
justify-content:center;
gap:6px;
font-size:15px;
font-weight:900;
box-shadow:0 10px 24px rgba(255,107,107,.35);
pointer-events:auto;
}

.fab span{
font-size:22px;
line-height:1;
}

/* 하단 네비 */

.bottom-nav{
position:fixed;
bottom:0;
left:50%;
transform:translateX(-50%);
width:100%;
max-width:430px;
height:72px;
background:rgba(255,255,255,.96);
backdrop-filter:blur(18px);
border-top:1px solid #EFE7E2;
display:flex;
justify-content:space-around;
align-items:center;
padding:8px 12px;
z-index:9998;
border-radius:0 0 30px 30px;
}

.nav-item{
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
gap:4px;
color:#A0A0A0;
font-size:11px;
font-weight:700;
}

.nav-item.active{
color:#FF6B6B;
}

.nav-icon{
font-size:22px;
line-height:1;
}

/* 버튼 */

div.stButton > button{
width:100%;
border-radius:14px;
font-weight:800;
border:1px solid #EFE7E2;
background:white;
color:#444;
height:42px;
}

div.stButton > button[kind="primary"]{
background:#FF6B6B;
color:white;
border:none;
box-shadow:0 4px 12px rgba(255,107,107,.25);
}

/* 입력 */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input{
border-radius:14px !important;
border:1px solid #EFE7E2 !important;
background:white !important;
}

div[data-testid="stSelectbox"] div{
border-radius:14px !important;
border-color:#EFE7E2 !important;
}

/* 모달 */

.modal-card{
background:white;
border-radius:24px;
padding:22px;
border:1px solid #F3ECE8;
box-shadow:0 10px 30px rgba(0,0,0,.08);
margin-bottom:18px;
}

.modal-title{
font-size:20px;
font-weight:900;
margin-bottom:18px;
}

</style>
    """, unsafe_allow_html=True)
