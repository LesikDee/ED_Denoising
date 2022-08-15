import numpy as np
def make_f_measure_report(true_buffer, denoised_ed_tuple):
    ed0 = denoised_ed_tuple[0]
    name = ed0.name.split('.')[0]
    n = len(ed0.buffer)
    #true_buffer = np.reshape(true_buffer, (ed0.header.fields["NS"], ed0.header.fields["NR"], ed0.header.fields["NC"]))
    with open(''.join([name, 'Chim_report.txt']), 'w') as f:


        #calculate
        for ed in denoised_ed_tuple:
            TP = 0
            TN = 0
            FP = 0
            FN = 0

            method = ed.name.split('_')[1]
            tr = ed.header.mean + ed.header.stddev
            for i in range(n):
                val = ed.buffer[i]

                if val < tr and not true_buffer[i]:
                    TN += 1
                elif val >= tr and true_buffer[i]:
                    TP += 1
                elif val < tr and true_buffer[i]:
                    FN += 1
                elif val >= tr and not true_buffer[i]:
                    FP += 1

            precision = TP /(TP + FP)
            recall =  TP /(TP + FN)
            f_measure = 2.0 * precision * recall /(precision + recall)

            tpr = TP /(TP +FN)
            tnr = TN /(TN + FP)
            bal_accuracy = (tpr + tnr) / 2
            # write to file
            f.write('Denoise method: ' + method + ':\n')
            f.write('True Positive: ' + str(TP) + '\n')
            f.write('False Negative: ' + str(FN) + '\n')
            f.write('False Positive: ' + str(FP) + '\n')
            f.write('True Negative: ' + str(TN) + '\n\n')
            f.write('Precision: ' + str(precision) + '\n')
            f.write('Recall: ' + str(recall) + '\n')
            f.write('F1 measure: ' + str(f_measure) + '\n\n')

            f.write('Balanced accuracy: ' + str(bal_accuracy) + '\n//////////////////////////////\n')

            print('ok')