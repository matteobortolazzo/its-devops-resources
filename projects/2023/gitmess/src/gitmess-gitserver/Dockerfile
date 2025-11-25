FROM ubuntu:latest

# Install SSH and Git
RUN apt-get update && apt-get install -y openssh-server git

# Create a user for SSH logins and repository access
RUN useradd -m gituser && echo "gituser:password" | chpasswd

# Set up SSH for the user
RUN mkdir -p /run/sshd
RUN mkdir /home/gituser/.ssh && chmod 700 /home/gituser/.ssh
RUN echo "PermitRootLogin no" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "AllowUsers gituser" >> /etc/ssh/sshd_config
RUN ssh-keygen -A

# Expose the SSH port
EXPOSE 22

# Set up a volume for repositories
VOLUME /data/git/repositories
RUN mkdir /data && mkdir /data/git/ && mkdir /data/git/repositories/ 
RUN chown -R gituser:gituser /data/git/repositories
RUN chmod -R 755 /data/git/repositories
WORKDIR /data/git/repositories

# Start SSH
CMD ["/usr/sbin/sshd", "-D"]
