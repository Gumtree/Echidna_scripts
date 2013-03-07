PRO max_write_gsas_ech,file_out,w
;***
;procedure to write the 1D workspace (w) in the standard gsas format
; for d2b and d1a, this is similar to the dat format
; see PRO write_dat
; output file is file_out

; file header is
; title
; "BANK"/"1"/nb.of.points/nb.of.lines in file/"CONST"/2theta(0)x100/2theta_step x100/"0"/"0"/"STD"

; get structure (title, errors etc) associated with workspace w and store them in the local structure datp
take_datp, datp

;calculate parameters for header
npoints=n_elements(w)
nlines=ceil(npoints/10)
two_theta_0=datp.x(0)*100.
;step=abs(datp.x(0)-datp.x(1))*100.
step=abs(float(round(1000*(datp.x(49)-datp.x(0))/49))/10)

;transform errors into "number of times measured"
;number of counts/error^2
nerr=intarr(npoints)
nerr=round(w/datp.e^2)

;open file and write header
openw,u,file_out,/get_lun
printf,u,datp.w_tit
printf,u,format='("BANK 1",2i8," CONST",2f10.3,"   0.0 0.0 STD")',npoints,nlines,two_theta_0,step ;other pars

;write number of times measured, counts in 10 columns
last=fix(npoints/10)*10
for i=0,last-1,10 do begin
printf,u,format='(10(i8))', $
round(w(i)),round(w(i+1)),round(w(i+2)),round(w(i+3)),round(w(i+4)),round(w(i+5)),round(w(i+6)),round(w(i+7)),round(w(i+8)), round(w(i+9))
endfor
rest=npoints-last
;if rest <>0 then last line to write will be incomplete
if (rest ne 0) then begin
   vec=intarr(2*rest)
   for i=0,rest-1 do begin vec(2*i)=nerr(last+i) &  vec(2*i+1)=w(last+i) &  endfor
   printf,u,format='('+strtrim(string(rest),2)+'(i2,i6))',vec
endif

;close file
free_lun, u

print,!stime
end
