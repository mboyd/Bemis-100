for i = 1:100
plot(real(ifft(real(A*exp(1i*i*pi/50)))))
ylim([-1,1])
pause(0.01)
end