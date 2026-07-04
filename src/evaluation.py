from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    average_precision_score,
    accuracy_score
)
def evalution_model(m, X, y):
    y_pred= m.predict(X)
    y_pred_proba= m.predict_proba(X)[:,1]
    acc= accuracy_score(y,y_pred)
    prec=precision_score(y,y_pred,zero_division=0)
    recall= recall_score(y,y_pred,zero_division=0)
    f1=f1_score(y,y_pred, zero_division=0)
    roc= roc_auc_score(y,y_pred_proba)
    ave= average_precision_score(y,y_pred_proba)
    c=confusion_matrix(y,y_pred)
    return {
        'accuracy' : acc,
        'precision'  : prec,
        'recall'    : recall,
        'F1' : f1,
        'ROC-AUC': roc,
        'PR-AUC' : ave,
        'confusion matrix' : c
    }   
