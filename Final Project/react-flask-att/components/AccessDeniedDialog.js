import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';

const AccessDeniedDialog = () => {
    return (
        <Dialog open onClose={() => console.log('Close dialog')}>
            <DialogTitle>Access Denied</DialogTitle>
            <DialogContent>
                You do not have permission to view this page.
            </DialogContent>
            <DialogActions>
                <Button onClick={() => window.history.back()}>Go Back</Button>
            </DialogActions>
        </Dialog>
    );
};

export default AccessDeniedDialog;
