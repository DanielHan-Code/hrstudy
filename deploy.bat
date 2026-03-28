@echo off
chcp 65001 >nul
echo.
echo ============================
echo   HR Study 배포 스크립트
echo ============================
echo.

REM src/ 원본 → 루트로 복사
copy /Y src\index.html index.html >nul
copy /Y src\leadership.html leadership.html >nul
copy /Y src\topics.html topics.html >nul
copy /Y src\references.html references.html >nul
copy /Y src\papers.html papers.html >nul

echo [1/3] 원본 파일 복사 완료

REM staticrypt 암호화
call node_modules\.bin\staticrypt index.html leadership.html topics.html references.html papers.html -p 0803 --remember 30 -d . --short >nul 2>&1

echo [2/3] 암호화 완료

REM git 커밋 & 푸시
git add index.html leadership.html topics.html references.html papers.html papers.json
git commit -m "콘텐츠 업데이트"
git push origin main

echo.
echo [3/3] 배포 완료!
echo.
pause
