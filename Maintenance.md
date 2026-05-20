# Sngce Workflow VPS Guide

## Architecture

### Frontend
- React/Vite
- Nginx
- HTTPS enabled

### Backend
- Node.js / Express
- PM2
- Nginx reverse proxy
- MongoDB Atlas

## Server Access

### Frontend VPS
```bash
ssh appuser@187.127.139.224
```

### Backend VPS
```bash
ssh appuser@187.127.139.222
```

## Deployment

### Frontend Deployment
```bash
cd ~/frontend
bash deploy.sh
```
- pull latest repo changes
- install dependencies
- build frontend
- copy dist files to nginx root
- restart nginx

### Backend Deployment
```bash
cd ~/backend
bash deploy.sh
```
- pull latest repo changes
- install dependencies
- restart PM2 backend process

## Environment Variables

### Frontend
```bash
nano Sngce_Workflow/frontend/.env
```
Important:
- Vite variables MUST start with `VITE_`
- rebuild frontend after changing `.env`

### Backend
```bash
nano Sngce_Workflow/backend/.env
```
Restart backend after modifying:
```bash
pm2 restart backend
```

## PM2 Commands

### List processes
```bash
pm2 list
```

### Restart backend
```bash
pm2 restart backend
```

### Stop backend
```bash
pm2 stop backend
```

### Delete backend process
```bash
pm2 delete backend
```

### View logs
```bash
pm2 logs backend
```

### Monitor processes
```bash
pm2 monit
```

### Save PM2 process list
```bash
pm2 save
```

### Startup on reboot
```bash
pm2 startup
```

## Nginx Commands

### Test config
```bash
sudo nginx -t
```

### Restart nginx
```bash
sudo systemctl restart nginx
```

### Reload nginx
```bash
sudo systemctl reload nginx
```

### Check nginx status
```bash
sudo systemctl status nginx
```

### View nginx logs
```bash
sudo tail -f /var/log/nginx/error.log
```

### View access logs
```bash
sudo tail -f /var/log/nginx/access.log
```

### Nginx config locations
- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

## SSL / Certbot

### Renew certificates manually
```bash
sudo certbot renew
```

### Check certbot timer
```bash
sudo systemctl status certbot.timer
```

### List certificates
```bash
sudo certbot certificates
```

## Useful Commands
```bash
free -h
top
```

### Better process monitor
```bash
htop
```
Install:
```bash
sudo apt install htop -y
```

### Check disk usage
```bash
df -h
```

### Check server uptime
```bash
uptime
```

### Check listening ports
```bash
sudo ss -tulnp
```

### Reboot server
```bash
sudo reboot
```

## Troubleshooting

### Frontend not updating
```bash
bash deploy.sh
sudo systemctl restart nginx
```

### Backend changes not reflecting
```bash
pm2 restart backend
pm2 logs backend
```

### API not reachable
```bash
pm2 list
sudo ss -tulnp
sudo systemctl status nginx
```

### SSL issues
```bash
sudo certbot certificates
sudo nginx -t
```

## Security Notes
- Use non-root user
- Keep `.env` out of GitHub
- Restrict CORS to frontend domain
- Use HTTPS for frontend + backend
- Keep MongoDB Atlas IP whitelist updated
