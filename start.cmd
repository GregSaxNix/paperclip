@echo off
title Paperclip Server
chcp 65001 >nul
set PAPERCLIP_ALLOW_TRUSTED_LAN=true
set PYTHONUTF8=1
cd /d D:\paperclip
pnpm dev
