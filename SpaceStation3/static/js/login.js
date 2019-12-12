var Auth = {
	vars: {
		//获取文档中 class="lowin" 的元素
		lowin: document.querySelector('.lowin'),
		lowin_brand: document.querySelector('.lowin-brand'),
		lowin_wrapper: document.querySelector('.lowin-wrapper'),
		lowin_login: document.querySelector('.lowin-login'),
        //获取文档中 class="lowin" 的元素
		lowin_wrapper_height: 0,
		login_back_link: document.querySelector('.login-back-link'),
		forgot_link: document.querySelector('.forgot-link'),
		login_link: document.querySelector('.login-link'),
		login_btn: document.querySelector('.login-btn'),
		register_link: document.querySelector('.register-link'),
		password_group: document.querySelector('.password-group'),
		password_group_height: 0,
		lowin_register: document.querySelector('.lowin-register'),
		lowin_footer: document.querySelector('.lowin-footer'),
		box: document.getElementsByClassName('lowin-box'),
		option: {}
	},
	//定义一个register函数，参数传入e对象
	register(e) {
		//在原有的类上，增加另一个类名
		Auth.vars.lowin_login.className += ' lowin-animated';
		setTimeout(() => {
			Auth.vars.lowin_login.style.display = 'none';
		}, 500);
		//将.lowin_register类的style中的display属性修改成block块元素
		Auth.vars.lowin_register.style.display = 'block';
        //在原有的类上，增加另一个类名
		Auth.vars.lowin_register.className += ' lowin-animated-flip';
		//调用auth类中的setHeight函数，传入（offsetHeight+offsetHeight）参数
		Auth.setHeight(Auth.vars.lowin_register.offsetHeight + Auth.vars.lowin_footer.offsetHeight);
		//取消事件的默认动作。
		//prevent预防，阻止
		e.preventDefault();
	},
	//定义一个login函数，参数传入e对象
	login(e) {
		//移除一个类名
		Auth.vars.lowin_register.classList.remove('lowin-animated-flip');
		//增加一个类名
		Auth.vars.lowin_register.className += ' lowin-animated-flipback';
		//设置类名中的style中的display属性的值为block
		Auth.vars.lowin_login.style.display = 'block';
		//移除一个类名
		Auth.vars.lowin_login.classList.remove('lowin-animated');
		//增加一个类名
		Auth.vars.lowin_login.className += ' lowin-animatedback';
		//设置一个定时器setTimeout(code,millisec)
		//code为代码块
        //millisec在执行代码前，需等待的，毫秒数
		setTimeout(() => {
			//该类名中的style中的display属性中的值修改成none
			Auth.vars.lowin_register.style.display = 'none';
		}, 500);
        //设置一个定时器setTimeout(code,millisec)
        //code为代码块
        //millisec在执行代码前，需等待的，毫秒数
		setTimeout(() => {
			//移除一个类名
			Auth.vars.lowin_register.classList.remove('lowin-animated-flipback');
			Auth.vars.lowin_login.classList.remove('lowin-animatedback');
		//	1000毫秒也就是1秒之后执行
		},1000);
		//调用面向对象中的类中的setHeight函数
		Auth.setHeight(Auth.vars.lowin_login.offsetHeight + Auth.vars.lowin_footer.offsetHeight);
		//取消，prevent阻止，取消时间的默认动作
		e.preventDefault();
	},
    //定义一个forgot函数，参数传入e对象
	forgot(e) {
		//增加一个类名
		Auth.vars.password_group.classList += ' lowin-animated';
		//修改类名中的style属性中的display属性中的值
		Auth.vars.login_back_link.style.display = 'block';
        //设置一个定时器setTimeout(code,millisec)
        //code为代码块
        //millisec在执行代码前，需等待的，毫秒数
		setTimeout(() => {
			Auth.vars.login_back_link.style.opacity = 1;
			Auth.vars.password_group.style.height = 0;
			Auth.vars.password_group.style.margin = 0;
		//	100毫秒后执行
		}, 100);
		//将被选择的对象的innerText属性设置成xxx值
		Auth.vars.login_btn.innerText = '忘记密码';
		//调用面向对象中的类的setHeight方法
		Auth.setHeight(Auth.vars.lowin_wrapper_height - Auth.vars.password_group_height);
		//获取DOM树中的元素，并setAttribute设置该对象的(属性，值)
		Auth.vars.lowin_login.querySelector('form').setAttribute('action', Auth.vars.option.forgot_url);
		//取消默认实践
		e.preventDefault();
	},
    //定义一个loginback函数，参数传入e对象
	loginback(e) {
		//移除元素对象中的类名
		Auth.vars.password_group.classList.remove('lowin-animated');
		//增加DOM元素对象的类名
		Auth.vars.password_group.classList += ' lowin-animated-back';
		//对DOM元素对象中的style属性的dispaly值修改成block块
		Auth.vars.password_group.style.display = 'block';
		//设置一个定时器
		//setTimeout(code，millisecond（毫秒）)
		setTimeout(() => {
			//代码块
			Auth.vars.login_back_link.style.opacity = 0;
			Auth.vars.password_group.style.height = Auth.vars.password_group_height + 'px';
			Auth.vars.password_group.style.marginBottom = 30 + 'px';
		//	100毫秒后执行
		}, 100);
		//设置第二个定时器,1000毫秒后面执行
		setTimeout(() => {
			//1000毫秒后执行的代码块
			Auth.vars.login_back_link.style.display = 'none';
			Auth.vars.password_group.classList.remove('lowin-animated-back');
		}, 1000);
		//对DOM元素中的innerText属性的值设置成:登入账号
		Auth.vars.login_btn.innerText = '登入账号';
		//获取DOM树中的元素并且设置属性和值
		Auth.vars.lowin_login.querySelector('form').setAttribute('action', Auth.vars.option.login_url);
		//调用类中的setHeight中的值
		Auth.setHeight(Auth.vars.lowin_wrapper_height);
		//取消默认动作
		e.preventDefault();
	},
	//定义一个setHeight函数
	setHeight(height) {
		Auth.vars.lowin_wrapper.style.minHeight = height + 'px';
	},
    //定义一个brand函数
	brand() {
		//增加一个类名
		Auth.vars.lowin_brand.classList += ' lowin-animated';
		//启用定时器
		setTimeout(() => {
			Auth.vars.lowin_brand.classList.remove('lowin-animated');
		}, 1000);
	},
	//定义一个init函数，option作为参数
	init(option) {
		Auth.setHeight(Auth.vars.box[0].offsetHeight + Auth.vars.lowin_footer.offsetHeight);

		Auth.vars.password_group.style.height = Auth.vars.password_group.offsetHeight + 'px';
		Auth.vars.password_group_height = Auth.vars.password_group.offsetHeight;
		Auth.vars.lowin_wrapper_height = Auth.vars.lowin_wrapper.offsetHeight;
		//将传入的option参数传入Auth.vars.option
		Auth.vars.option = option;
		Auth.vars.lowin_login.querySelector('form').setAttribute('action', option.login_url);

		var len = Auth.vars.box.length - 1;

		for(var i = 0; i <= len; i++) {
			if(i !== 0) {
				//循环为box中的元素增加类名
				Auth.vars.box[i].className += ' lowin-flip';
			}
		}
		//为该元素对象增加一个事件监听
		Auth.vars.forgot_link.addEventListener("click", (e) => {
			Auth.forgot(e);
		});
        //为该元素对象增加一个事件监听
		Auth.vars.register_link.addEventListener("click", (e) => {
			Auth.brand();
			Auth.register(e);
		});
        //为该元素对象增加一个事件监听
		Auth.vars.login_link.addEventListener("click", (e) => {
			Auth.brand();
			Auth.login(e);
		});
        //为该元素对象增加一个事件监听
		Auth.vars.login_back_link.addEventListener("click", (e) => {
			Auth.loginback(e);
		});
	}
}