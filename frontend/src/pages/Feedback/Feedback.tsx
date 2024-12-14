import { FeedbackCard } from "../../components/Cards/FeedbackCard/FeedbackCard";
import { PageContainer } from "../../components/containers/PageContainer";
import { MainButton } from "../../components/UI/MainButton/MainButton";
import styles from './Feedback.module.scss';
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useEffect } from "react";
import { FeedbackForm, Question } from "../../models/entities";
import { useCreateFeedbackMutation, useGetAllQuestionsQuery } from "../../api/feedbackSlice";
import clsx from "clsx";
import { AppModal } from "../../components/AppModal/AppModal";
import { FeedbackModalForm } from "./FeedbackForm/FeedbackModalForm";
import { useToggler } from "../../hooks/useToggler";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { MapComponent } from "../../components/MapComponent";
import { SkeletonFeedbackCard } from "../../components/Cards/FeedbackCard/SkeletonFeedbackCard";
import { initialFormData, validationSchema } from "./initialFormData";
import { useFormik } from "formik";
import { useSnackbar } from "../../hooks/useSnackbar";

export const FeedbackPage = () => {
    const navigate = useNavigate();
    const { openStatus, handleClose, handleOpen } = useToggler();
    const { t, getTranslatedAspectName, getTranslatedQuestion } = useAppTranslator();
    const { data, isLoading: isLoadingCards } = useGetAllQuestionsQuery();

    const {openInfo} = useSnackbar()

    
    



    const {errors, touched,  values, handleSubmit: openPopup, setValues, setFieldTouched, setFieldValue} = useFormik({
        initialValues: initialFormData.ratings,
        validationSchema,
        onSubmit() {handleOpen()},
    })

    useEffect(() => {
        if (data) {
            const questionsTemplates = data.results.map(({ id, rating_required }: Question) => ({
                question_id: id,
                answer: '',
                rating: rating_required ? 0 : undefined
            }));
            setValues(questionsTemplates)
        }
    }, [data]);

    const [sendForm, { isLoading, isSuccess }] = useCreateFeedbackMutation();

    useEffect(() => {
        if (isSuccess) {
            navigate(ROUTE.THANK_FOR_FEEDBACK);
        }
    }, [isSuccess, navigate]);


    const handleClick = (index: number, value: number) => {
        setFieldValue(`${index}.rating`, value)
    };
    
    const handleChange = (index: number, value: string) => {
        setFieldValue(`${index}.answer`, value)
    };
    
  
    const handleBlur = (index: number) => {
        setFieldTouched(`${index}.rating`, true)
    }

    const handleSubmit = (f: Omit<FeedbackForm, 'ratings'>) => {
        sendForm({...f, ratings: values});
    };

    const handleNextStep = () => {
        const isConsistErrors = !!Object.keys(errors).length
        if(isConsistErrors){
            window.scrollTo({
                top: 0,
                behavior: 'smooth' 
              });
            openInfo(t('check_feedback_list'), 'error')
        }
    }
 
    return (
        <>
            <PageContainer className={clsx({ [styles.loading]: isLoading })}>
                <div className={styles.intro}>
                    <p>{t('greetting')}<span>  KOLORYT!</span></p>
                    <p>{t('ask_to_rate')}</p>
                    <p>P.S {t('ps')}</p>
                </div>
                <form 
                    className={styles.cardContainer}
                    id={'feedback'}
                    onSubmit={openPopup}
                >
                    {isLoadingCards ? (
                        <MapComponent qty={7} component={<SkeletonFeedbackCard />} />
                    ) : (
                        data?.results.map(({ id, aspect_name_en, aspect_name_uk, question_en, question_uk, rating_required }, index) => (
                            <FeedbackCard
                                key={id}
                                tabIndex={index}
                                isError = {!!(touched[index]?.rating && errors[index]?.rating)}
                                question1={`${index + 1}. ${rating_required ? getTranslatedAspectName(aspect_name_en ?? "", aspect_name_uk ?? "") : getTranslatedQuestion(question_en ?? "", question_uk ?? "")}`} 
                                question2={rating_required ? getTranslatedQuestion(question_en ?? "", question_uk ?? ""): undefined}
                                showButtons={rating_required}
                                thisRating={values.find(({ question_id }) => question_id === id)?.rating} 
                                onClick={(val) => handleClick(index, val)} 
                                onChangeText={(val) => handleChange(index, val)}
                                onBlur={handleBlur}
                            />
                        ))
                    )}
                </form>
                <div className={styles.actions}>
                    <MainButton
                        type="submit"
                        form = 'feedback'
                        color="blue"
                        title={t("send")}
                        onClick={handleNextStep}
                    />
                    <button className={styles.button} onClick={() => navigate(ROUTE.HOME)}>{t('close_and_return')}</button>
                </div>
            </PageContainer>
            <AppModal open={openStatus} onClickOutside={handleClose}>
                <FeedbackModalForm
                    isLoading={isLoading}
                    onSubmit={handleSubmit}
                />
            </AppModal>
        </>
    );
};