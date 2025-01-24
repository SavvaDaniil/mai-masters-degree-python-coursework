

class UserService {

    /**
     * Обновление данных профиля пользователем
     */
    async profileUpdate(csrftoken, formData, setIsLoading, setWarning){
        setIsLoading(true);
        setWarning("Идет загрузка...");

        let isError = false;
        try
        {
            return await fetch("/api/user/profile", {
                method : "POST",
                headers: {'X-CSRFToken': csrftoken},
                body: formData
            })
            .then(response => response.json())
            .then(baseResponse => {
                if(typeof(baseResponse["error"]) !== "undefined" && baseResponse["error"] != null && baseResponse["error"] !== "")
                {
                    setWarning(baseResponse["error"]);
                    isError = true;
                }
            })
        } catch(error)
        {
            console.log(error);
            isError = true;
        } finally
        {
            setIsLoading(false);
            if(!isError){
                setWarning("Успешно сохранено");
            }
        }
    }
}