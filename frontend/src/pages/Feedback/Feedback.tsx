import { FeedbackCard } from "../../components/Cards/FeedbackCard/FeedbackCard";
import { PageContainer } from "../../components/containers/PageContainer";
import { MainButton } from "../../components/UI/MainButton/MainButton";
import styles from './Feedback.module.scss';
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useEffect, useState } from "react";
import { FeedbackForm, Question } from "../../models/entities";
import { useCreateFeedbackMutation, useGetAllQuestionsQuery } from "../../api/feedbackSlice";
import clsx from "clsx";
import { AppModal } from "../../components/AppModal/AppModal";
import { FeedbackModalForm } from "./FeedbackForm/FeedbackModalForm";
import { useToggler } from "../../hooks/useToggler";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { MapComponent } from "../../components/MapComponent";
import { SkeletonFeedbackCard } from "../../components/Cards/FeedbackCard/SkeletonFeedbackCard";

export const FeedbackPage = () => {
    const navigate = useNavigate();
    const { openStatus, handleClose, handleOpen } = useToggler();
    const { t, getTranslatedAspectName, getTranslatedQuestion } = useAppTranslator();
    const { data, isLoading: isLoadingCards } = useGetAllQuestionsQuery();

    const [form, setForm] = useState<FeedbackForm>({
        email: '',
        name: '',
        comment: '',
        ratings: [] 
    });

    const translatedLabels = {
        name: t("name"),
        email: t("email"),
        comment: t("comment")
    };

    console.log('ratings', form.ratings);
    

    useEffect(() => {
        if (data) {
            const questionsTemplates = data.results.map(({ id, rating_required }: Question) => ({
                question_id: id,
                answer: '',
                rating: rating_required ? 0 : undefined
            }));
            setForm((prevForm) => ({ ...prevForm, ratings: questionsTemplates }));
        }
    }, [data]);

    const [sendForm, { isLoading, isSuccess }] = useCreateFeedbackMutation();

    console.log(data);
    

    useEffect(() => {
        if (isSuccess) {
            navigate(ROUTE.THANK_FOR_FEEDBACK);
        }
    }, [isSuccess, navigate]);

    const handleClick = (id: number, value: number) => {
        setForm((prevForm) => ({
            ...prevForm,
            ratings: prevForm.ratings.map((rating) =>
                rating.question_id === id ? { ...rating, rating: value } : rating
            )
        }));
        console.log(`Updated rating for question ID ${id}: ${value}`); // Log for debugging
    };
    
    const handleChange = (id: number, value: string) => {
        setForm((prevForm) => ({
            ...prevForm,
            ratings: prevForm.ratings.map((rating) =>
                rating.question_id === id ? { ...rating, answer: value } : rating
            )
        }));
    };
    
    
    const handleSubmit = () => {
        console.log("Submitting form data:", JSON.stringify(form));
        sendForm(form); 
    };

    const handleChangeHeader = (fieldName: string, value: string) => {
        setForm((prevForm) => ({ ...prevForm, [fieldName]: value }));
    };
 

    return (
        <>
            <PageContainer className={clsx({ [styles.loading]: isLoading })}>
                <div className={styles.intro}>
                    <p>{t('greeting')}<span>KOLORYT!</span></p>
                    <p>{t('ask_to_rate')}</p>
                    <p>P.S {t('ps')}</p>
                </div>
                <div className={styles.cardContainer}>
                    {isLoadingCards ? (
                        <MapComponent qty={7} component={<SkeletonFeedbackCard />} />
                    ) : (
                        data?.results.map(({ id, aspect_name_en, aspect_name_uk, question_en, question_uk, rating_required }, index) => (
                            <FeedbackCard
                                key={id || index}
                                question1={`${index + 1}. ${rating_required ? getTranslatedAspectName(aspect_name_en ?? "", aspect_name_uk ?? "") : getTranslatedQuestion(question_en ?? "", question_uk ?? "")}`} 
                                question2={rating_required ? getTranslatedQuestion(question_en ?? "", question_uk ?? ""): undefined}
                                showButtons={rating_required}
                                thisRating={form.ratings.find(({ question_id }) => question_id === id)?.rating} 
                                onClick={(val) => handleClick(id, val)} 
                                onChangeText={(val) => handleChange(id, val)}
                            />
                        ))
                    )}
                </div>
                <div className={styles.actions}>
                    <MainButton
                        color="blue"
                        title={t("send")}
                        onClick={handleOpen}
                    />
                    <button className={styles.button} onClick={() => navigate(ROUTE.HOME)}>{t('close_and_return')}</button>
                </div>
            </PageContainer>
            <AppModal open={openStatus} onClickOutside={handleClose}>
                <FeedbackModalForm
                    isLoading={isLoading}
                    onSubmit={handleSubmit}
                    onChange={handleChangeHeader}
                    translatedLabels={translatedLabels}  // Pass translated labels to FeedbackModalForm
                />
            </AppModal>
        </>
    );
};
