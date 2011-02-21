pos = zeros(100,1);
vel = zeros(100,1);
acc = zeros(100,1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initial configuration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

T = .1; % "Tension" 
mu = 1; % "mass per length"
friction = 0.01; % frictional force per velocity
dt = .1;

% Full sine wave 
for i=1:100
    pos(i) = sin((i-1)*2*pi/99);
end

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

% Impulse, ends
% for i = 2:10
%     pos(i) = sin((i-2)*pi/8);
% end
% for i = 91:99
%     pos(i) = sin((i-91)*pi/8);
% end

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
    ylim([-1,1])
    pause(0.0001);
    for i = 2:99
        acc(i) = ((pos(i+1)-2*pos(i)+pos(i-1))*T-friction*vel(i))/mu;
    end

    for i = 2:99
        vel(i) = (vel(i) + acc(i)*dt);
    end

    for i = 2:99
        pos(i) = pos(i) + vel(i)*dt;
    end
    
end



    