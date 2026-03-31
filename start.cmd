@echo off
title Paperclip Server
chcp 65001 >nul
set PAPERCLIP_ALLOW_TRUSTED_LAN=true
set PYTHONUTF8=1
set NODE_OPTIONS=--input-type=module
cd /d D:\paperclip
pnpm dev
