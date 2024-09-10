import style from './style.module.scss'
import {TextField} from "@mui/material";
import { PageContainer } from "../../components/containers/PageContainer"
import {useNavigate} from "react-router-dom";


const textFieldStyles = {
    '& .MuiInputLabel-root': { fontSize: '24px' },
    '& .MuiInputBase-root': { height: '50px' },
    '& .MuiInputBase-input': { padding: '16px 0' },
};

export const Contact = () => {

    const navigate = useNavigate(); // Инициализируем хук navigate

    const handleButtonClick = () => {
        navigate('/sendcontacts'); // Переход на страницу /sendcontacts
    };

    return (
        <PageContainer>
            <div className={style.titleContainer}>
                <p className={style.description}>
                    Вас вітає
                    <span className={style.name}> KOLORYT ,</span> <br/>
                    сподіваємось що ви так само насолоджуетесь нашими виробами як і ми !
                </p>
            </div>
            <div className={style.generalContainer}>
                <div className={style.contactScontainer}>
                    <h3>Контакти</h3>
                    <p className={style.subTitle}>Зв’яжіться з нами: </p>
                    <p> Instagram </p>
                    <p> Facebook </p>
                    <p className={style.subTitle}> Номер телефону: </p>
                    <p> +380634578932 </p>
                    <p className={style.subTitle}> Для співпраці: </p>
                    <p> koloryt@gmail.com </p>
                    <p className={style.subTitle}> Підтримка: </p>
                    <p> customer@koloryt.com </p>
                </div>
                <div className={style.formContainer }>
                    <h2> Є запитання? Зв‘яжіться з нами... </h2>
                    <div className={style.frame}>
                        <TextField
                            id="standard-name"
                            label="Ім'я"
                            variant="standard"
                            sx={textFieldStyles}
                        />
                        <TextField
                            label="E-mail"
                            variant="standard"
                            sx={textFieldStyles}
                        />
                        <TextField
                            label="Номер телефону"
                            variant="standard"
                            sx={textFieldStyles}
                        />
                        <TextField
                            label="Ваше повідомлення"
                            variant="standard"
                            sx={textFieldStyles}
                        />
                        <button className={style.sendButton} onClick={handleButtonClick}>Надіслати</button>
                    </div>
                </div>
            </div>
        </PageContainer>

    );
};
