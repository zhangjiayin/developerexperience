package org.opensource.freepic.servlet;

import java.io.IOException;
import java.io.InputStream;
import java.util.Date;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.fileupload.FileItemIterator;
import org.apache.commons.fileupload.FileItemStream;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.apache.commons.io.IOUtils;
import org.opensource.freepic.bean.Photo;
import org.opensource.freepic.dao.PhotoDao;

import com.google.appengine.api.datastore.Blob;


/**
 * 
 * @author	DualR
 * @mail	dualrs@gmail.com
 * @site	http://www.mimaiji.com
 */

@SuppressWarnings("serial")
public class PhotoServlet extends HttpServlet {
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		String method = req.getParameter("method");
		Long id = null;
		// display photo
		if (method.equals("show")) {
			id = Long.parseLong(req.getParameter("id"));
			if (id == null) {
				return;
			}
			Photo photo = PhotoDao.getInstance().getById(id);
			if (photo == null) {
				return;
			}
			Blob b = photo.getPhoto();
			resp.setContentType("image/jpeg;charset=utf-8");
			resp.getOutputStream().write(b.getBytes());
			resp.getOutputStream().close();
		}
		// edit photo property
		if (method.equals("edit")) {
			id = Long.parseLong(req.getParameter("id"));
			if (id == 0 || id == null) {
				resp.sendRedirect("index");
			}
			if (req.getMethod().equals("GET")) {
				Photo photo = null;
				photo = PhotoDao.getInstance().getById(id);
				req.setAttribute("photo", photo);
				try {
					req.getRequestDispatcher("photoEdit.jsp")
							.forward(req, resp);
				} catch (ServletException e) {
					e.printStackTrace();
				}
			}
		}
		// delete photo
		if (method.equals("delete")) {
			id = Long.parseLong(req.getParameter("id"));
			PhotoDao.getInstance().deleteById(id);
			resp.sendRedirect("index");
		}

	}

	public void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		// upload photo and save in datastore
		String method = req.getParameter("method");
		if (method.equals("upload")) {
			ServletFileUpload upload = new ServletFileUpload();
			FileItemIterator iterator = null;
			try {
				iterator = upload.getItemIterator(req);
			} catch (FileUploadException e) {
				e.printStackTrace();
			}
			try {
				while (iterator.hasNext()) {
					FileItemStream item = iterator.next();
					InputStream stream = item.openStream();
					if (item.isFormField()) {
						// Handle form field
					} else {
						// Handle the uploaded file
						Blob bImg = new Blob(IOUtils.toByteArray(stream));
						Date date = new Date();
						String title = item.getName();
						Photo photo = new Photo(title, date, bImg);

						// Photo photo = new PhotobImg);
						PhotoDao.getInstance().insertPhoto(photo);
						resp.sendRedirect("index");
					}
				}
			} catch (FileUploadException e) {
				e.printStackTrace();
			}

		}
		// edit and update photo property
		if (method.equals("edit")) {
			Long id = Long.parseLong(req.getParameter("id"));
			if (id == 0 || id == null) {
				resp.sendRedirect("index");
			}
			String title = req.getParameter("title");
			String description = req.getParameter("description");
			Date date = new Date();
			Photo photo = new Photo(id, title, description, date);
			PhotoDao.getInstance().update(photo);
			resp.sendRedirect("index");
		}
	}
}