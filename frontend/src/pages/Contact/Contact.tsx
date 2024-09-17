import style from './style.module.scss'
import {TextField} from "@mui/material";
import { PageContainer } from "../../components/containers/PageContainer"
import {useNavigate} from "react-router-dom";
import {useTranslation} from "react-i18next";
import {useState} from "react";


const textFieldStyles = {
    '& .MuiInputLabel-root': { fontSize: '24px' },
    '& .MuiInputBase-root': { height: '50px' },
    '& .MuiInputBase-input': { padding: '16px 0' },
};

export const Contact = () => {

    const navigate = useNavigate();
    const { t } = useTranslation();

    const [name, setName] = useState('');
    const [error, setError] = useState(false);
    const [email, setEmail] = useState('');
    const [error2, setError2] = useState(false);
    const [phone, setPhone] = useState('');
    const [error3, setError3] = useState(false);
    const [message, setMessage] = useState('');
    const [error4, setError4] = useState(false);

    // const data = {
    //     name,
    //     email,
    //     phone,
    //     message
    // };
    //
    // const handleButtonClick = async () => {
    //     try {
    //         const response = await fetch('http://localhost:8000/api/comments/comments', {  // Замените на ваш URL
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify(data),
    //         });
    //
    //         if (response.ok) {
    //             setSubmitSuccess('Форма успешно отправлена');
    //             navigate('/success'); // Переход на страницу успеха
    //         } else {
    //             setSubmitSuccess('Ошибка при отправке формы');
    //         }
    //     } catch (error) {
    //         console.error('Ошибка:', error);
    //         setSubmitSuccess('Ошибка при отправке формы');
    //     }
    // };

    const handleButtonClick = () => {
        navigate('/sendcontacts');
    };


    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;

        if (/\d/.test(value)) {
            setError(true);
        } else {
            setError(false);
        }
        setName(value);
    };

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setEmail(value);

        if (!emailRegex.test(value)) {
            setError2(true);
        } else {
            setError2(false);
        }
    };

    const phoneRegex = /^\+?\d{10,15}$/;

    const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setPhone(value);

        if (!phoneRegex.test(value)) {
            setError3(true);
        } else {
            setError3(false);
        }
    };

    const handleMessageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setMessage(value);
        setError4(value.trim() === '');
    };

    return (
        <PageContainer>
            <div className={style.titleContainer}>
                <p className={style.description}>
                    {t('hello_part_1')}
                    <span className={style.name}> KOLORYT,</span> <br/>
                    {t('hello_part_2')}
                </p>
            </div>
            <div className={style.generalContainer}>
                <div className={style.contactScontainer}>
                    <h3>{t('contacts')}</h3>
                    <p className={style.subTitle}>{t('contact_us')} </p>
                    <p> Instagram </p>
                    <p> Facebook </p>
                    <p className={style.subTitle}>{t('phone')}
                    </p>
                    <p> +380634578932 </p>
                    <p className={style.subTitle}> {t('for_cooperation')} </p>
                    <p> koloryt@gmail.com </p>
                    <p className={style.subTitle}> {t('support')} </p>
                    <p> customer@koloryt.com </p>
                </div>
                <div className={style.formContainer }>
                    <h2> {t('have_question')} </h2>
                    <div className={style.frame}>
                        <TextField
                            id="standard-name"
                            label={t('name')}
                            variant="standard"
                            sx={textFieldStyles}
                            value={name}
                            onChange={handleNameChange}
                            error={error}
                            helperText={error ? 'Ім`я не повинно містити цифри' : ''}
                        />
                        <TextField
                            label={t('email')}
                            variant="standard"
                            sx={textFieldStyles}
                            value={email}
                            onChange={handleEmailChange}
                            error={error2}
                            helperText={error2 ? 'Введіть валідний email' : ''}
                            required
                        />
                        <TextField
                            label={t('phone')}
                            variant="standard"
                            sx={textFieldStyles}
                            onChange={handlePhoneChange}
                            value={phone}
                            error={error3}
                            helperText={error2 ? 'Введіть валідний телефон' : ''}
                        />
                        <TextField
                            label={t('message')}
                            variant="standard"
                            sx={textFieldStyles}
                            value={message}
                            onChange={handleMessageChange}
                            error={error4}
                        />
                        <button className={style.sendButton}
                                onClick={handleButtonClick}
                                disabled={error2 || !email}>
                            {t('send')}
                        </button>
                    </div>
                </div>
            </div>
        </PageContainer>
    );
};
