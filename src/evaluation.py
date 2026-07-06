from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    average_precision_score,
    accuracy_score
)
import numpy as np 
def evaluate_at_threshold(X,
    y_true,
    y_proba,
    threshold,
    review_cost_per_application,
    default_loss_rate,
    review_effectiveness):

    y_pred = (y_proba >= threshold).astype(int)

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred,zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    roc_auc = roc_auc_score(y_true, y_proba)
    pr_auc = average_precision_score(y_true, y_proba)

    flagged_rate= np.mean(y_pred)

    fn_loan_amounts = X.loc[(y_true == 1) & (y_pred == 0), 'loan_amnt']
    fn_loss = fn_loan_amounts.sum() * default_loss_rate
    
    tp_loan_amounts = X.loc[(y_true == 1) & (y_pred == 1), 'loan_amnt']
    tp_residual_loss = tp_loan_amounts.sum() * default_loss_rate * (1 - review_effectiveness)

    review_total_cost= (fp + tp) * review_cost_per_application
    total_cost = fn_loss + tp_residual_loss + review_total_cost
    return {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1),
        'roc_auc': float(roc_auc),
        'pr_auc': float(pr_auc),
        'fn_loss': float(fn_loss),
        'tp_residual_loss': float(tp_residual_loss),
        'review_total_cost': float(review_total_cost),
        'total_cost': float(total_cost),
        'flagged_rate': float(flagged_rate),
        'fn_count': int(fn),
        'fp_count': int(fp),
        'tp_count': int(tp),
        'tn_count': int(tn),
        'confusion_matrix': cm.tolist()
    }
