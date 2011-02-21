pos = zeros(100,1);
vel = zeros(100,1);
acc = zeros(100,1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initial configuration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

T = .01; % "Tension" 
decay = 0.0008; % fraction of velocity lost per tick

% Full sine wave 
% for i=1:100
%     pos(i) = sin((i-1)*2*pi/99);
% end

% Half sine wave 
% for i=1:100
%     pos(i) = sin((i-1)*pi/99);
% end

% 
% for i = 40:60
%     pos(i) = 1;
% end

% Impulse, center
% pos(50) = 1;

% Impulse, end
for i = 2:10
    pos(i) = 1;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Run and Plot
%%%%%%%%%%%%%%%%%%%%%%%%%%%%



figure
subplot 211

while 1
    subplot 211
    plot(pos)
    ylim([-1,1]);
    subplot 212
    plot(abs(pos))
    ylim([0,1])
    pause(0.001);
    for i = 2:99
        acc(i) = ((pos(i+1)-pos(i))-(pos(i)-pos(i-1)))*T;
    end

    for i = 2:99
        vel(i) = (vel(i) + acc(i))*(1-decay);
    end

    for i = 2:99
        pos(i) = pos(i) + vel(i);
    end
    
end



    